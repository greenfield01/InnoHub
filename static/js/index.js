// $(document).ready(function () {
//     const id = $('#delete-btn').attr("data-id")
//     const $container = $('#container-post');
//     $('#delete-btn').on('click', function () {
//         $.ajax({
//             url: `/post/delete/${id}`,
//             type: "POST",
//             data: { post_id: id }
//         })
//             .done(function () {
//                 $('#deleteModal').hide()
//                 location.href = 'home.html'
//             })
//             .fail(function (err) {
//                 console.log("Error deleting item")
//             });
//     });
// });