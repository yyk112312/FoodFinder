// document.getElementById("1").addEventListener("click", function() {
//     // console.log('card clicked')
//     document.getElementById("1").innerHTML = ABC
//   });

// $(document).ready(function() {
//     var button = $('#myBtn');
//     $(button).prop('disabled', true);

//     $('.click').click(function() {
//         console.log('card is clicked');
//         if ($(button).prop('disabled')) $(button).prop('disabled', false);
//     });

//     $(button).click(function() {
//         if ($(button).prop('disabled')) alert("button is disabled");
//     });
// });
$(document).on("click", "select-btn", function () {
    var myId = $(this).data('id');
    console.log(myId)
    $(".modal-body #food_item").val( myId );
});
