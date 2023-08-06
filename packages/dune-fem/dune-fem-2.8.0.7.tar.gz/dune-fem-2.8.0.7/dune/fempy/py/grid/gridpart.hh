#ifndef DUNE_FEMPY_PY_GRID_GRIDPART_HH
#define DUNE_FEMPY_PY_GRID_GRIDPART_HH

#include <cassert>

#include <map>
#include <string>
#include <type_traits>
#include <utility>

#include <dune/grid/io/file/vtk/vtkwriter.hh>

#include <dune/fem/misc/l2norm.hh>
#include <dune/fem/gridpart/common/gridpartadapter.hh>
#include <dune/fem/storage/singleton.hh>

#include <dune/python/grid/hierarchical.hh>
#include <dune/python/grid/vtk.hh>

#include <dune/fempy/pybind11/pybind11.hh>

namespace Dune
{

  namespace FemPy
  {

    namespace detail
    {

      // GridModificationListener
      // ------------------------

      template< class Grid >
      class GridModificationListener final
        : public Python::GridModificationListener< Grid >
      {
        typedef Fem::DofManager< Grid > DofManager;

      public:
        GridModificationListener ( const Grid &grid )
          : dofManager_( DofManager::instance( grid ) )
        {}
        virtual ~GridModificationListener ( )
        {}

        virtual void postModification ( const Grid &grid )
        {
          dofManager_.resize();
          dofManager_.compress();
        }

      private:
        DofManager &dofManager_;
      };



      // addGridModificationListener
      // ---------------------------

      template< class Grid >
      inline static void addGridModificationListener ( const Grid &grid )
      {
        typedef GridModificationListener< Grid > Listener;
        for( const auto &listener : Python::detail::gridModificationListeners( grid ) )
        {
          if( dynamic_cast< Listener * >( listener ) )
            return;
        }
        // get python handle for the given grid (must exist)
        pybind11::handle nurse = pybind11::detail::get_object_handle( &grid, pybind11::detail::get_type_info( typeid( Grid ) ) );
        assert(nurse);
        Python::detail::addGridModificationListener( grid, new Listener(grid), nurse );
      }



      // GridPartConverter
      // -----------------

      template< class GV >
      struct GridPartConverter
      {
        typedef GV GridView;
        typedef Fem::GridPartAdapter< GV > GridPart;

        GridPart &operator() ( pybind11::handle gridView )
        {
          auto result = instances_.emplace( gridView.ptr(), nullptr );
          auto pos = result.first;
          if( result.second )
          {
            GridView* view = gridView.template cast< GridView* >();

            // create new gridpart object
            pos->second = new GridPart( *view );
            // add grid modification listener (if not registered)
            addGridModificationListener( view->grid() );

            // create Python guard object, removing the grid part once the grid view dies
            pybind11::cpp_function remove_gridpart( [ this, pos ] ( pybind11::handle weakref ) {
                delete pos->second;
                instances_.erase( pos );
                weakref.dec_ref();
              } );
            pybind11::weakref weakref( gridView, remove_gridpart );
            weakref.release();
          }
          assert( pos->second );
          return *pos->second;
        }

      private:
        std::map< PyObject *, GridPart * > instances_;
      };


      template< class GP >
      struct GridPartConverter< Dune::GridView< Fem::GridPart2GridViewTraits< GP > > >
      {
        typedef GP GridPart;
        typedef Dune::GridView< Fem::GridPart2GridViewTraits< GP > > GridView;

        GridPart &operator() ( pybind11::handle gridView )
        {
          return const_cast< GridPart & >( gridView.template cast< GridView* >()->impl().gridPart() );
        }
      };

      // gridView is already a wrapped gridPart
      // issue: need to be able to retrieve the gridView wrapper from a given gridPart
      template< class GP >
      struct GridPartConverter< Fem::GridPart2GridViewImpl< GP > >
      {
        typedef GP GridPart;
        typedef Fem::GridPart2GridViewImpl< GP > GridView;

        GridPart &operator() ( pybind11::handle gridView )
        {
          return const_cast< GridPart & >( gridView.template cast< GridView* >()->gridPart() );
        }
      };

      // gridPartConverter singleton storage
      // -----------------------------------

      template< class GridView >
      inline GridPartConverter< GridView > &gridPartConverter ()
      {
        return Dune::Fem::Singleton< GridPartConverter<GridView> > :: instance();
      }

    } // namespace detail



    // GridPart
    // retrieve (or construct) gridPart from given givenView
    // --------

    template< class GridView >
    using GridPart = typename detail::GridPartConverter< GridView >::GridPart;

    template< class GridView >
    inline static GridPart< GridView > &gridPart ( pybind11::handle gridView )
    {
      return detail::gridPartConverter< GridView >()( std::move( gridView ) );
    }

    template< class GridView >
    inline static GridPart< GridView > &gridPart ( const GridView &gridView )
    {
      return gridPart< GridView >( pybind11::detail::get_object_handle( &gridView, pybind11::detail::get_type_info( typeid( GridView ) ) ) );
    }

    // constructGridPart (returns a gridView)
    // --------------------------------------
    template< class GridPart, class... Args >
    inline static auto constructGridPart ( Args &&... args )
    {
      return new typename GridPart::GridViewType( Fem::GridPart2GridViewImpl< GridPart >( std::forward< Args >( args )... ) );
    }
  } // namespace FemPy

} // namespace Dune

#endif // #ifndef DUNE_FEMPY_PY_GRID_GRIDPART_HH
