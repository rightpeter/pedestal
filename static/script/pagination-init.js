$('#pagination-demo').twbsPagination({
        totalPages: total_pages,
        visiblePages: visible_pages,
        version: '1.1',
        startPage: current_page,
        onPageClick: function (event, page) {
            if (page != startPage){
                window.location.href = "index?page=" + page;
            }
        }
});
