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