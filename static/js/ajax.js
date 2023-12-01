// Code start for add to bag
$(".addToBag").click(function (event) {
    event.preventDefault(); // Prevent the default action of the link

    // let id = $(".addToBag").attr("data-menu-id");

    let id = $(this).attr("data-menu-id");
    let myData = { id: id };
    console.log(myData);

    $.ajax({
        url: '/bag/add-to-bag/' + id,
        data: myData,

        success: function (data) {

            if (data.status) {
                // alert('Item added successfully!');
                Swal.fire({ icon: 'success', text: 'Item added!' })
            }
            else {
                alert('Error: ' + response.error);
            }
        }
    });
});
// Code end for add to bag


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
            Swal.fire({ icon: 'warning', text: 'Email is required' });
        }
        else if (!sbj) {
            Swal.fire({ icon: 'warning', text: 'Subject is required' });
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
$("#signup").click(function () {
    event.preventDefault(); // Prevent the default form submission behavior

    console.log("Signup clicked");
    let uname = $("#uname").val();
    let email = $("#email").val();
    let mobile = $("#mobile").val();
    let utype = $("#utype").val();
    let pwd = $("#pwd").val();
    let pwdc = $("#pwdc").val();
    let csr = $("input[name=csrfmiddlewaretoken]").val();

    if (!uname || !email || !mobile || !utype || !pwd || !pwdc) {
        Swal.fire({ icon: 'warning', text: 'All fields are required.' });
    }

    let myData = { uname: uname, email: email, mobile: mobile, utype: utype, pwd: pwd, pwdc: pwdc, csrfmiddlewaretoken: csr }

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
})
// Code end for signup page


// Code start for signin page
$(document).ready(function () {
    $("#signin").click(function (event) {
        event.preventDefault(); // Prevent the default form submission behavior

        let uname = $("#uname").val();
        let pwd = $("#pwd").val();
        let csr = $("input[name=csrfmiddlewaretoken]").val();
        
        let myData = { uname:uname, pwd:pwd, csrfmiddlewaretoken: csr };

        if(!uname){
            Swal.fire({icon:"warning", text:"Please enter username!"})
        }
        else if(!pwd){
            Swal.fire({icon:"warning", text:"Please enter password!"})
        }
        else{
            $.ajax({
                url: '/login/',
                method: 'POST',
                data: myData,
                success: function (data) {
                    if (data.status === "signIn") {
                        Swal.fire({icon: 'success', text: 'Signin successfully' });
                        $("form")[0].reset();
                    }
    
                    else if(data.status === "invalidUser"){
                        Swal.fire({icon: "warning", text: "Invalid username or password. Please try again."})
                    }
                }
            });
        }
    });
});
// Code end for signin page

