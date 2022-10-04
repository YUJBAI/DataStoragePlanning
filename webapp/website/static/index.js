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

function openForm() {
  document.getElementById("myForm").hidden = false;
  document.getElementById("myTable").hidden = true;
}

function closeForm() {
  document.getElementById("myTable").hidden = false;
  document.getElementById("myForm").hidden = true;
}

$('form.update_form').on('submit', function () {
  console.log($('.form-id').val())
  $j.ajax({
    url: '/update',
    type: 'POST',
    data: {
      'id': $('.form-id').val(),
      'name': $('.form-name').val(),
      'data_generated': $('.form-data_generated').val(),
      'price': $('.form-price').val(),
      'lifetime': $('.form-lifetime').val(),
      'start_date': $('.form-start_date').val(),
      'initial_size': $('.form-initial_size').val()
    },
    success: function (response) {
      if (response == 1) {
        swal({
          title: "Save Successfully!",
          icon: "success",
          button: "Keep going!"
        }).then((value) => {
          window.location.reload()
        });
      } else {
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

$(document).ready(function () {
  $('#insert_form').on("submit", function (event) {
    event.preventDefault();
    if ($('#instrument').val() == "") {
      swal({
        title: "Name is required!",
        text: "Please fill up the name",
        icon: "warning",
        button: "Try again!"
      });
    }
    else if ($('#dataGenerated').val() == '') {
      swal({
        title: "Data generated per day is required!",
        text: "Please fill up the data generated per day",
        icon: "warning",
        button: "Try again!"
      });
    }
    else if (isNaN($('#dataGenerated').val())) {
      swal({
        title: "Data generated per day has to be a number!",
        text: "Please fill up the correct type of data generated per day",
        icon: "warning",
        button: "Try again!"
      });
    }
    else if ($('#price').val() == '') {
      swal({
        title: "Instrument's price is required!",
        text: "Please Fill Up The Instrument's Price",
        icon: "warning",
        button: "Try again!"
      });
    }
    else if (isNaN($('#price').val())) {
      swal({
        title: "Price has to be a number!",
        text: "Please fill up the correct type of price",
        icon: "warning",
        button: "Try again!"
      });
    }
    else if ($('#lifetime').val() == '') {
      swal({
        title: "Expected Lifetime is Required!",
        text: "Please Fill Up The DExpected Lifetimed",
        icon: "warning",
        button: "Try again!"
      });
    }
    else if (isNaN($('#lifetime').val())) {
      swal({
        title: "Lifetime has to be a number!",
        text: "Please fill up the correct type of lifetime",
        icon: "warning",
        button: "Try again!"
      });
    }
    else if ($('#startDate').val() == '') {
      swal({
        title: "Start date is required!",
        text: "Please fill up the start date",
        icon: "warning",
        button: "Try again!"
      });
    }
    else if (!(/(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})/gi).test($('#startDate').val())) {
      swal({
        title: "Start date has to follow the format!",
        text: "Please fill up the start date with DD/MM/YYYY format, and it has to be valid",
        icon: "warning",
        button: "Try again!"
      });
    }
    else if ($('#initialSize').val() == '') {
      swal({
        title: "Initial data size is required!",
        text: "Please Fill Up The Initial Data Size",
        icon: "warning",
        button: "Try again!"
      });
    }
    else if (isNaN($('#initialSize').val())) {
      swal({
        title: "Initial size has to be a number!",
        text: "Please fill up the correct type of initial size",
        icon: "warning",
        button: "Try again!"
      });
    }
    else {
      $j.ajax({
        url: "/insert",
        method: "POST",
        data: $('#insert_form').serialize(),
        dataType: 'json',
        beforeSend: function () {
          $('#insert').val("Inserting");
        },
        success: function (data) {
          $('#add_data_Modal').modal('hide');
          if (data == 'success') {

            swal({
              title: "Success Added!",
              icon: "success",
            }).then((value) => {
              window.location.href = "/";
            });
          } else {
            swal({
              title: "Something Wrong!",
              icon: "warning",
            })
          }
        }
      });
    };
  });
});