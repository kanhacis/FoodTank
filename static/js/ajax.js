// Code start for contact page
$(document).ready(function () {
    $("#sendMsg").click(function (event) {
        event.preventDefault(); // Prevent the default form submission behavior

        let name = $("#name").val();
        let email = $("#email").val();
        let sbj = $("#subject").val();
        let msg = $("#message").val();
        let csr = $("input[name=csrfmiddlewaretoken]").val();

        if (!email) {
            Swal.fire({ icon: 'warning', text: 'Email is required', timer:1000, showCancelButton: false, showConfirmButton: false});
        }
        else if (!sbj) {
            Swal.fire({ icon: 'warning', text: 'Subject is required', timer:1000, showCancelButton: false, showConfirmButton: false});
        }
        else {
            let myData = { name: name, email: email, subject: sbj, message: msg, csrfmiddlewaretoken: csr };

            $.ajax({
                url: '/contact/',
                method: 'POST',
                data: myData,
                success: function (data) {
                    if (data.status === "Save") {
                        Swal.fire({
                            icon: 'success',
                            title: 'Success',
                            text: 'Message sent successfully',
                            timer:1000, showCancelButton: false, showConfirmButton: false
                        })
                    }
                }
            });
        }
        $("form")[0].reset();
    });
});
// Code end for contact page


// Code start for signup page
$("#signup").click(function (event) {
    event.preventDefault(); // Prevent the default form submission behavior

    let uname = $("#uname").val();
    let email = $("#email").val();
    let mobile = $("#mobile").val();
    let utype = $("#utype").val();
    let pwd = $("#pwd").val();
    let pwdc = $("#pwdc").val();
    let csr = $("input[name=csrfmiddlewaretoken]").val();

    let myData = { uname: uname, email: email, mobile: mobile, utype: utype, pwd: pwd, pwdc: pwdc, csrfmiddlewaretoken: csr }

    if (!uname || !email || !mobile || !utype || !pwd || !pwdc) {
        Swal.fire({ icon: 'warning', text: 'All fields are required.', timer:1000, showCancelButton: false, showConfirmButton: false});
    }
    else if(pwd != pwdc){
        Swal.fire({icon:"error", text:"Password and confirm password does not match", timer:1000, showCancelButton: false, showConfirmButton: false})
    }
    else{
        $.ajax({
            url: '/signup/',
            method: 'POST',
            data: myData,
            success: function (data) {
                if (data.status === "createAccount") {
                    Swal.fire({ icon: 'success', text: 'Account created successfully' })
                }
                else if (data.status === "userExist") {
                    Swal.fire({ icon: 'warning', text: 'User already exist.' });
                }
                else if (data.status === "emailExist") {
                    Swal.fire({ icon: "warning", text: "Email already exist." })
                }
                else if (data.status === "mobileExist") {
                    Swal.fire({ icon: "warning", text: "Contact no. already exist." })
                }
                else if (data.status === "passwordNotMatch") {
                    Swal.fire({ icon: "warning", text: "Password and confirm password do not match." })
                }
            }
        })
        $("form")[0].reset();
    }
})
// Code end for signup page


// Code start for signin page
$(document).ready(function () {
    $("#signin").click(function (event) {
        event.preventDefault(); // Prevent the default form submission behavior

        let uname = $("#uname").val();
        let pwd = $("#pwd").val();
        let csr = $("input[name=csrfmiddlewaretoken]").val();

        let myData = { uname: uname, pwd: pwd, csrfmiddlewaretoken: csr };

        if (!uname) {
            Swal.fire({ icon: "warning", text: "Please enter username!", timer:1000, showCancelButton: false, showConfirmButton: false})
        }
        else if (!pwd) {
            Swal.fire({ icon: "warning", text: "Please enter password!", timer:1000, showCancelButton: false, showConfirmButton: false})
        }
        else {
            $.ajax({
                url: '/login/',
                method: 'POST',
                data: myData,
                success: function (data) {
                    if (data.status === "signIn") {
                        window.location = '/';
                    }

                    else if (data.status === "invalidUser") {
                        Swal.fire({ icon: "warning", text: "Invalid username or password. Please try again.", timer:1000, showCancelButton: false, showConfirmButton: false})
                    }
                }
            });
        }
    });
});
// Code end for signin page


// Code start for profile update
$("#updateProfile").click(function (event) {
    event.preventDefault();

    let uname = $("#uname").val();
    let email = $("#email").val();
    let fname = $("#fname").val();
    let lname = $("#lname").val();
    let mobile = $("#mobile").val();
    let utype = $("#utype").val();
    let state = $("#state").val();
    let city = $("#city").val();
    let area = $("#area").val();
    let zipcode = $("#zipcode").val();
    let house = $("#house").val();
    let profile = $("#getProfile").val();
    let category = $("#category").val();
    let csr = $("input[name=csrfmiddlewaretoken]").val();

    let myData = {
        uname: uname, email: email, fname: fname, lname: lname, mobile: mobile,
        utype: utype, primary:'True', state: state, city: city, area: area, zipcode: zipcode,
        house: house, profile:profile, category: category, csrfmiddlewaretoken: csr
    }

    console.log(profile, house);

    if(!city || !area || !house){
        Swal.fire({icon:"warning", text:"You can not empty city, area, house no.", timer:1000, showCancelButton: false, showConfirmButton: false});
    }
    else{
        $.ajax({
            url: "/profile/",
            method: "POST",
            data: myData,
            success: function (data) {
                if (data.status) {
                    Swal.fire({ icon: "success", text: "Profile update successfuly!", timer:1000, showCancelButton: false, showConfirmButton: false })
                }
                else {
                    Swal.fire({ icon: "error", text: "Something went wrong try again!", timer:1000, showCancelButton: false, showConfirmButton: false })
                }
            }
        })
    }
})
// Code end for profile update


// ***************** Code start for add to bag *************************
// Function to update the item count and list in the UI
var count = ''
function updateUI(data) {
    count = data.bagItemCount;
    $("#itemCount").text(count);

    // Update the counter of navbar
    $("#counter").text(count);

    let result = '';
    let x = data.bagFoodsName;
    for(let i = 0; i < x.length; i++){
        result += `<div class="list-item">${x[i]}</div>`;
    }

    $("#listContainer").html(result);
}

$(".addToBag").click(function (event) {
    event.preventDefault();

    let id = $(this).attr("data-menu-id");
    let myData = { id: id };

    $(this).closest(".inBag").find(".addText").text("Added move to bag ➙");

    $.ajax({
        url: '/bag/add-to-bag/' + id,
        data: myData,
        success: function (data) {
            if (data.status == "itemAdded") {
                Swal.fire({ icon: 'success', text: 'Item added!', timer: 500, showCancelButton: false, showConfirmButton: false});

                // Update the item count in localStorage
                localStorage.setItem('itemCount', data.bagItemCount);

                // Update the list of items in localStorage
                localStorage.setItem('bagFoodsName', JSON.stringify(data.bagFoodsName));

                // Update the UI
                updateUI(data);
            }
            else {
                Swal.fire({ icon: 'error', text: 'Item already in the bag!', timer: 500, showCancelButton: false, showConfirmButton: false});
            }
        }
    });
});

// Check if there is stored data on page load and update the UI
$(document).ready(function() {
    let storedCount = localStorage.getItem('itemCount');
    let storedItems = localStorage.getItem('bagFoodsName');

    if (storedCount && storedItems) {
        let itemCount = parseInt(storedCount);
        let itemsArray = JSON.parse(storedItems);

        let storedData = {
            bagItemCount: itemCount,
            bagFoodsName: itemsArray
        };

        updateUI(storedData);
    }
});

// Clear the localStorage when user logout
$("#userLogout").click(function () { 
    localStorage.clear();
})
// ******************** Code end for add to bag ********************** 



// ************* Code start for listing current added item ******************
$(document).ready(function () {
    var circle = $('#circle');
    var listContainer = $('#listContainer');

    circle.mouseenter(function () {
        // Toggle the visibility of the list container
        listContainer.slideDown();
    });

    circle.mouseleave(function () {
        // Toggle the visibility of the list container
        listContainer.slideUp();
    });

    circle.click(function () { 
        // Move to the basket
        window.location = "/bag/view_bag/";
     })
});
// ************* Code end for listing current added item ******************



// ************ Code start to delete a basket item ****************
$(".deleteFood").click(function (event) {
    event.preventDefault();

    let id = $(this).attr("data-food-item");
    let foodName = $(this).attr("data-food-name");
    console.log(foodName);
    let myData = { id: id };

    $.ajax({
      url: "/bag/deleteItem/" + id,
      data: myData,
      success: function (data) {
        if (data.status === "itemDeleted") { 
          // Remove the complete row
          $(this).closest(".deleteRow").remove();

          // Update the total price in the HTML
          $(".totalPrice").text("₹" + data.finalPrice);

          // Update itemCount in localStorage
          let itemCount = parseInt(localStorage.getItem('itemCount'), 10) || 0;
          if (itemCount > 0) {
            localStorage.setItem('itemCount', String(itemCount - 1));
          }

          // Update the counter of navbar
          $("#counter").text(itemCount-=1);

          // Remove selected food name from localStorage
          let selectedFoodName = data.deletedFoodName; // Assuming it's retrieved from the server response
          let storedFoods = JSON.parse(localStorage.getItem('bagFoodsName')) || [];
          let updatedFoods = storedFoods.filter(food => food !== foodName); // Use the foodName passed in the AJAX call
          localStorage.setItem('bagFoodsName', JSON.stringify(updatedFoods));

          // Update the UI (if needed)
          $("#itemCount").text("items " + String(parseInt(data.totalItem, 10) - 1));
        }
      }.bind(this)
    });
  });

  $("#userLogout").click(function () { 
    localStorage.clear();
   })
// ************ Code end to delete a basket item ***************



// *************** Start code to increase item quantity **************
$(".itemQuantity").click(function (event) {
    event.preventDefault();

    let quantityElement = $(this);
    let currentQuantity = parseInt(quantityElement.val(), 10); // Get the current quantity as a number

    let id = $(this).attr("data-food-item");
    console.log(id, currentQuantity);

    if (currentQuantity < 1) {
      console.log("Quantity is less than 1");
      return;
    }

    let row = quantityElement.closest('tr'); // Find the closest <tr> element (row)
    let newPriceElement = row.find('.newPrice'); // Find the corresponding .newPrice element within the row

    $.ajax({
      url: "/bag/view_bag/",
      data: { id: id, quantity: currentQuantity },
      success: function (data) {
        let finalP = parseInt(data.price, 10);
        newPriceElement.text("₹" + finalP);

        $(".totalPrice").text("₹" + data.Final);
      }
    });
  });
// *************** End code to increase item quantity ****************