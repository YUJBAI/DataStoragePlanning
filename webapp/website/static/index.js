function deleteHistory(historyId) {
  fetch("/delete-history", {
    method: "POST",
    body: JSON.stringify({ historyId: historyId }),
  }).then((_res) => {
    swal({
      title: "Success Deleted",
      icon: "success",
    }).then((value) => {
      window.location.href = "/";
    });
  });
}

function deleteStorage(storageId) {
  fetch("/delete-storage", {
    method: "POST",
    body: JSON.stringify({ storageId: storageId }),
  }).then((_res) => {
    swal({
      title: "Success Deleted",
      icon: "success",
    }).then((value) => {
      window.location.href = "/setting";
    });
  });
}

//function deleteData(Id) {
//  fetch("/delete", {
//    method: "POST",
//    body: JSON.stringify({ Id: Id }),
//  }).then((_res) => {
//    window.location.href = "/setting";
//  });
//}

function getOption() {
  selectElement = document.querySelector('#select-table');
  output = selectElement.value;
  document.querySelector('.output').textContent = output;
}

function openForm(){
  document.getElementById("myForm").hidden = false;
  document.getElementById("myTable").hidden = true;  
}

function closeForm(){
  document.getElementById("myTable").hidden = false;
  document.getElementById("myForm").hidden = true;  
}

$('form.update_form').on('submit', function (){
  console.log($('.form-id').val())
  $j.ajax({
      url: '/update',
      type: 'POST',
      data:{
          'id': $('.form-id').val(),
          'name': $('.form-name').val(),
          'data_generated': $('.form-data_generated').val(),
          'price': $('.form-price').val(),
          'lifetime': $('.form-lifetime').val(),
          'start_date': $('.form-start_date').val(),
          'initial_size': $('.form-initial_size').val()
      },
      success:function (response){
          if(response == 1){
              swal({
                title: "Save Successfully!",
                icon: "success",
                button: "Keep going!"
              }).then((value) => {
                window.location.reload()
              });
          }else{
            swal({
              title: "Something Wrong!",
              text: "Please try again!",
              icon: "warning",
              button: "Try again!"
            });
          }
      }
  })
  event.preventDefault();
});

$(document).ready(function(){
  $('#insert_form').on("submit", function(event){
   event.preventDefault();
   if($('#instrument').val() == "")
   {
    swal({
      title: "Name is required!",
      text: "Please Fill Up The Name",
      icon: "warning",
      button: "Try again!"
    });
   }
   else if($('#dataGenerated').val() == '')
   {
    swal({
      title: "Data generated is required!",
      text: "Please Fill Up The Data Generated",
      icon: "warning",
      button: "Try again!"
    });
   }
   else if($('#price').val() == '')
   {
    swal({
      title: "Instrument's price is required!",
      text: "Please Fill Up The Instrument's Price",
      icon: "warning",
      button: "Try again!"
    });
   }
   else if($('#lifetime').val() == '')
   {
    swal({
      title: "Expected Lifetime is Required!",
      text: "Please Fill Up The DExpected Lifetimed",
      icon: "warning",
      button: "Try again!"
    });
   }
   else if($('#startDate').val() == '')
   {
    swal({
      title: "Start date is required!",
      text: "Please Fill Up The Start date",
      icon: "warning",
      button: "Try again!"
    });
   }
   else if($('#initialSize').val() == '')
   {
    swal({
      title: "Initial data size is required!",
      text: "Please Fill Up The Initial Data Size",
      icon: "warning",
      button: "Try again!"
    });
   }
   else
   {
    $j.ajax({
         url:"/insert",
         method:"POST",
         data:$('#insert_form').serialize(),
         dataType:'json',
         beforeSend:function(){
          $('#insert').val("Inserting");
         },
         success:function(data){
          $('#add_data_Modal').modal('hide');
           if (data=='success'){
              
            swal({
              title: "Success Deleted",
              icon: "success",
            }).then((value) => {
              window.location.href = "/";
            });
           }
          }
     });
    };
  });
 });