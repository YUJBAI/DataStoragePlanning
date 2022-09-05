function deleteHistory(historyId) {
  fetch("/delete-history", {
    method: "POST",
    body: JSON.stringify({ historyId: historyId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function deleteStorage(storageId) {
  fetch("/delete-storage", {
    method: "POST",
    body: JSON.stringify({ storageId: storageId }),
  }).then((_res) => {
    window.location.href = "/setting";
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
              alert("Save successfully");
              window.location.reload();
          }else{
              alert("Not saved");
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
    alert("Name is required");
   }
   else if($('#dataGenerated').val() == '')
   {
    alert("Data generated is required");
   }
   else if($('#price').val() == '')
   {
    alert("Instrument's price is required");
   }
   else if($('#lifetime').val() == '')
   {
    alert("Expected lifetime is required");
   }
   else if($('#startDate').val() == '')
   {
    alert("Start date is required");
   }
   else if($('#initialSize').val() == '')
   {
    alert("Initial data size is required");
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
               window.location.href = "/";
           }
          }
     });
    };
  });
 });