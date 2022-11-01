import {Card, CardBody, CardHeader, CardText, CardTitle} from "reactstrap";
import DataTable from "react-data-table-component";
import {columns} from "./list/columns";
import {ChevronDown} from "react-feather";
import ReactPaginate from "react-paginate";

const CustomPagination = () => {
    const count = 10;

    return (
        <ReactPaginate
            previousLabel={''}
            nextLabel={''}
            pageCount={count || 1}
            activeClassName='active'
            forcePage={0 !== 0 ? 0 - 1 : 0}
            // onPageChange={page => handlePagination(page)}
            pageClassName={'page-item'}
            nextLinkClassName={'page-link'}
            nextClassName={'page-item next'}
            previousClassName={'page-item prev'}
            previousLinkClassName={'page-link'}
            pageLinkClassName={'page-link'}
            containerClassName={'pagination react-paginate justify-content-end my-2 pe-1'}
        />
    )
}

const Okpd = () => {
    return (
        <Card>
            <CardHeader>
                <CardTitle>List okpd</CardTitle>
            </CardHeader>
            <CardBody>
                <div>
                    <Card className='overflow-hidden'>
                        <div className='react-dataTable'>
                            <DataTable
                                noHeader
                                subHeader
                                sortServer
                                pagination
                                responsive
                                paginationServer
                                // columns={columns}
                                // onSort={handleSort}
                                sortIcon={<ChevronDown />}
                                className='react-dataTable'
                                paginationComponent={CustomPagination}
                                // data={dataToRender()}
                                // subHeaderComponent={
                                //     <CustomHeader
                                //         store={store}
                                //         searchTerm={searchTerm}
                                //         rowsPerPage={rowsPerPage}
                                //         handleFilter={handleFilter}
                                //         handlePerPage={handlePerPage}
                                //         toggleSidebar={toggleSidebar}
                                //     />
                                // }
                            />
                        </div>
                    </Card>
                </div>
            </CardBody>
        </Card>
    )
}

export default Okpd;
