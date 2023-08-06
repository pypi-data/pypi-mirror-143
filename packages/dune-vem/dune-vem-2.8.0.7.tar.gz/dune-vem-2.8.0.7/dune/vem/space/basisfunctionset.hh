#ifndef DUNE_VEM_SPACE_BASISFUNCTIONSET_HH
#define DUNE_VEM_SPACE_BASISFUNCTIONSET_HH

#include <cassert>
#include <cstddef>

#include <algorithm>
#include <type_traits>
#include <utility>

#include <dune/geometry/referenceelements.hh>

#include <dune/fem/common/fmatrixcol.hh>
#include <dune/fem/quadrature/quadrature.hh>
#include <dune/fem/space/basisfunctionset/functor.hh>
#include <dune/fem/space/shapefunctionset/vectorial.hh>

#include <dune/vem/agglomeration/functor.hh>
#include <dune/vem/misc/vector.hh>

namespace Dune
{

  namespace Vem
  {

    // VEMBasisFunctionSet
    // -------------------

    // TODO: add template arguments for ValueProjection and JacobianProjection
    template< class Entity, class ShapeFunctionSet >
    class VEMBasisFunctionSet
    {
      typedef VEMBasisFunctionSet< Entity, ShapeFunctionSet > ThisType;

    public:
      typedef Entity EntityType;

      typedef typename ShapeFunctionSet::FunctionSpaceType FunctionSpaceType;

      typedef typename FunctionSpaceType::DomainFieldType DomainFieldType;
      typedef typename FunctionSpaceType::RangeFieldType RangeFieldType;

      typedef typename FunctionSpaceType::DomainType DomainType;
      typedef typename FunctionSpaceType::RangeType RangeType;
      typedef typename FunctionSpaceType::JacobianRangeType JacobianRangeType;
      typedef typename FunctionSpaceType::HessianRangeType HessianRangeType;

      static constexpr int dimDomain = DomainType::dimension;
      static constexpr int dimRange  = RangeType::dimension;

      typedef ReferenceElement< typename DomainType::field_type, dimDomain > ReferenceElementType;

      typedef FieldMatrix < DomainFieldType, dimDomain, dimDomain > HessianMatrixType;

      const auto& valueProjection() const { return (*valueProjections_)[agglomerate_]; }
      const auto& jacobianProjection() const { return (*jacobianProjections_)[agglomerate_]; }
      const auto& hessianProjection() const { return (*hessianProjections_)[agglomerate_]; }
      typedef Std::vector< Std::vector< DomainFieldType > > ValueProjection;
      typedef Std::vector< Std::vector< DomainType > > JacobianProjection;
      typedef Std::vector< Std::vector< HessianMatrixType > > HessianProjection;
      template <class T>
      using Vector = Std::vector<T>;

      VEMBasisFunctionSet () = default;

      VEMBasisFunctionSet ( const EntityType &entity,
                            int agglomerate,
                            std::shared_ptr<Vector<ValueProjection>> valueProjections,
                            std::shared_ptr<Vector<JacobianProjection>> jacobianProjections,
                            std::shared_ptr<Vector<HessianProjection>> hessianProjections,
                            ShapeFunctionSet shapeFunctionSet = ShapeFunctionSet() )
        : entity_( &entity ), //polygon
          agglomerate_(agglomerate),
          shapeFunctionSet_( std::move( shapeFunctionSet ) ),
          valueProjections_( valueProjections),
          jacobianProjections_( jacobianProjections ),
          hessianProjections_( hessianProjections ),
          size_( valueProjection()[0].size() * dimRange)
      {}

      int order () const { return shapeFunctionSet_.order(); }

      std::size_t size () const { return size_; }

      const ReferenceElementType &referenceElement () const
      {
        return referenceElement( entity().type() );
      }

      template< class Quadrature, class DofVector, class Values >
      void evaluateAll ( const Quadrature &quadrature, const DofVector &dofs, Values &values ) const
      {
        const std::size_t nop = quadrature.nop();
        for( std::size_t qp = 0; qp < nop; ++qp )
          evaluateAll( quadrature[ qp ], dofs, values[ qp ] );
      }

      template< class Point, class DofVector >
      void evaluateAll ( const Point &x, const DofVector &dofs, RangeType &value ) const
      {
        value = RangeType( 0 );
        shapeFunctionSet_.evaluateEach( position( x ), [ this, &dofs, &value ] ( std::size_t alpha, RangeType phi_alpha ) {
            for( std::size_t j = 0; j < size(); ++j )
              value.axpy( valueProjection()[ alpha ][ j ]*dofs[ j ], phi_alpha );
          } );
      }

      template< class Point, class Values > const
      void evaluateAll ( const Point &x, Values &values ) const
      {
        assert( values.size() >= size() );
        std::fill( values.begin(), values.end(), RangeType( 0 ) );
        shapeFunctionSet_.evaluateEach( position(x), [ this, &values ] ( std::size_t alpha, RangeType phi_alpha ) {
            for( std::size_t j = 0; j < size(); ++j )
              values[ j ].axpy( valueProjection()[ alpha ][ j ], phi_alpha );
          } );
      }

      // TODO: use lower order shape function set for Jacobian
      template< class Quadrature, class DofVector, class Jacobians >
      void jacobianAll ( const Quadrature &quadrature, const DofVector &dofs, Jacobians &jacobians ) const
      {
        const std::size_t nop = quadrature.nop();
        for( std::size_t qp = 0; qp < nop; ++qp )
          jacobianAll( quadrature[ qp ], dofs, jacobians[ qp ] );
      }

      template< class Point, class DofVector >
      void jacobianAll ( const Point &x, const DofVector &dofs, JacobianRangeType &jacobian ) const
      {
        jacobian = JacobianRangeType( 0 );
        shapeFunctionSet_.evaluateEach( position( x ), [ this, &dofs, &jacobian ] ( std::size_t alpha, RangeType phi_alpha ) {
            const auto &jacobianProjectionAlpha = jacobianProjection()[alpha];
            for( std::size_t j = 0; j < size(); ++j )
              jacobian[0].axpy( dofs[j]*phi_alpha[0], jacobianProjectionAlpha[j]);
          } );
      }

      template< class Point, class Jacobians > const
      void jacobianAll ( const Point &x, Jacobians &jacobians ) const
      {
        assert( jacobians.size() >= size() );
        std::fill( jacobians.begin(), jacobians.end(), JacobianRangeType( 0 ) );
        shapeFunctionSet_.evaluateEach( position(x), [ this, &jacobians ] ( std::size_t alpha, RangeType phi_alpha ) {
            const auto &jacobianProjectionAlpha = jacobianProjection()[alpha];
            for( std::size_t j = 0; j < size(); ++j )
              jacobians[j][0].axpy( phi_alpha[0], jacobianProjectionAlpha[j]);
        } );
      }

      template< class Quadrature, class DofVector, class Hessians >
      void hessianAll ( const Quadrature &quadrature, const DofVector &dofs, Hessians &hessians ) const
      {
        const std::size_t nop = quadrature.nop();
        for(std::size_t qp = 0; qp <nop; ++qp )
          hessianAll( quadrature[ qp ], dofs, hessians[ qp ] );
      }

      template< class Point, class DofVector >
      void hessianAll ( const Point &x, const DofVector &dofs, HessianRangeType &hessian ) const
      {
        hessian = HessianRangeType( 0 );
        shapeFunctionSet_.evaluateEach( position(x), [this, &dofs, &hessian ] ( std::size_t alpha, RangeType phi_alpha ) {
            const auto &hessianProjectionAlpha = hessianProjection()[alpha];
            for( std::size_t j = 0; j < size(); ++j )
              hessian[0].axpy( dofs[j]*phi_alpha[0], hessianProjectionAlpha[j]);
        } );
      }

      template< class Point, class Hessians > const
      void hessianAll ( const Point &x, Hessians &hessians ) const
      {
        assert( hessians.size() >= size() );
        std::fill( hessians.begin(), hessians.end(), HessianRangeType( 0 ) );
        shapeFunctionSet_.evaluateEach( position(x), [ this, &hessians ] ( std::size_t alpha, RangeType phi_alpha ) {
            const auto &hessianProjectionAlpha = hessianProjection()[alpha];
            for( std::size_t j = 0; j < size(); ++j )
              hessians[j][0].axpy( phi_alpha[0], hessianProjectionAlpha[j]);
        } );
      }

      const EntityType &entity () const { assert( entity_ ); return *entity_; }

      template< class Point, class Factor >
      void axpy ( const Point &x, const Factor &factor, DynamicVector<DomainType> &dofs ) const
      {
        shapeFunctionSet_.evaluateEach( position( x ), [ this, &factor, &dofs ] ( std::size_t alpha, RangeType phi_alpha ) {
            for( std::size_t j = 0; j < size(); ++j )
              dofs[ j ].axpy( phi_alpha[0]*valueProjection()[ alpha ][ j ], factor );
          } );
      }
      template< class Point, class Factor >
      void axpy ( const Point &x, const Factor &factor, DynamicVector<HessianMatrixType> &dofs ) const
      {
        shapeFunctionSet_.evaluateEach( position( x ), [ this, &factor, &dofs ] ( std::size_t alpha, RangeType phi_alpha ) {
            for( std::size_t j = 0; j < size(); ++j )
              for ( std::size_t l = 0; l < dimDomain; ++l )
                for ( std::size_t k = 0; k < dimDomain; ++k )
                  dofs[ j ][l][k] += phi_alpha[0] *
                      0.5*( jacobianProjection()[ alpha ][ j ][ k ]*factor[l] +
                            jacobianProjection()[ alpha ][ j ][ l ]*factor[k] );
          } );
      }
      template< class Point, class Factor >
      void axpy ( const Point &x, const DomainType &normal, const Factor &factor, DynamicVector<HessianMatrixType> &dofs ) const
      {
        shapeFunctionSet_.evaluateEach( position( x ), [ this, &factor, &dofs, &normal ] ( std::size_t alpha, RangeType phi_alpha ) {
            for( std::size_t j = 0; j < size(); ++j )
            {
              DomainFieldType Gn = 0;
              for ( std::size_t n = 0; n < dimDomain; ++n )
                Gn += phi_alpha[0] * jacobianProjection()[ alpha ][ j ][ n ]*normal[n];
              for ( std::size_t l = 0; l < dimDomain; ++l )
                for ( std::size_t k = 0; k < dimDomain; ++k )
                    dofs[ j ][l][k] += Gn * 0.5*(normal[k]*factor[l] + normal[l]*factor[k] );
            }
          } );
      }


    private:
      template< class Point >
      DomainType position ( const Point &x ) const
      {
        return Fem::coordinate(x);
      }

      const EntityType *entity_ = nullptr;
      std::size_t agglomerate_;
      ShapeFunctionSet shapeFunctionSet_;
      std::shared_ptr<Vector<ValueProjection>> valueProjections_;
      std::shared_ptr<Vector<JacobianProjection>> jacobianProjections_;
      std::shared_ptr<Vector<HessianProjection>> hessianProjections_;
      size_t size_;
    };

  } // namespace Vem

} // namespace Dune

#endif // #ifndef DUNE_VEM_SPACE_BASISFUNCTIONSET_HH
