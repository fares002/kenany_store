$('.plus-cart').click(function(){
    console.log('clicked');

    var id = $(this).attr("pid").toString();
    var quantity = this.parentNode.children[2]
    $.ajax({
        tybe: "GET",
        url: "/pluscart",
        data:{
            prod_id: id
        },
        success: function(data){
            console.log(data);
            quantity.innerText = data.quantity;
            document.getElementById(`quantity${id}`).innerText = data.quantity;
            document.getElementById(`amount_tt`).innerText = data.amount;
            document.getElementById("totalamount").innerText = data.total;

        }
    })
})

$('.minus-cart').click(function(){
    console.log('clicked');

    var id = $(this).attr("pid").toString();
    var quantity = this.parentNode.children[2]
    $.ajax({
        tybe: "GET",
        url: "/minuscart",
        data:{
            prod_id: id
        },
        success: function(data){
            console.log(data);
            quantity.innerText = data.quantity;
            document.getElementById(`quantity${id}`).innerText = data.quantity;
            document.getElementById(`amount_tt`).innerText = data.amount;
            document.getElementById("totalamount").innerText = data.total;

        }
    })
})


// $('.remove-cart').click(function(){
//     var id = $(this).attr("pid").toString();
//     var to_remove_element = this.parentNode.parentNode.parentNode.parentNode;


//     $.ajax({
//         type: "GET",
//         url: "/remove_cart_item",
//         data: {
//             prod_id: id
//         },
//         success: function(data){
        
//                 console.log(data);
//                 document.getElementById(`amount_tt`).innerText = data.amount;
//                 document.getElementById(`quantity${id}`).innerText = data.quantity;
//                 document.getElementById("totalamount").innerText = data.total;
//                 to_remove_element.remove();
//         }
// })
// })