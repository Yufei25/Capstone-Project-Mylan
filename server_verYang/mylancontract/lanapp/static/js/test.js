function populateList() {
    $.get("/lanapp/get-changes")
      .done(function(data) {
          var list = $("#contract-list");
          list.data('max-time', data['max-time']);
          // list.html('');

          getUpdates();

          // for (var i = 0; i < data.contracts.length; i++) {
          //     contract = data.contracts[i];
          //     var new_contract = $(contract.html);
          //     new_contract.data("contract-id", contract.id);
          //     list.prepend(new_contract);
          //     updateAllChildren(contract.id)
          // }
      });
}


function addContractComment(contract_id){
    var commentField = $("#contract-comment-field-"+contract_id);
    // console.log(commentField.val());
    $.post("/lanapp/contract-comment/" + contract_id, {comment: commentField.val()})
      .done(function(data) {
          updateListChild("contract-comment",contract_id)
      });
}

function addContentComment(content_id){
    addComment("content", content_id)
}

function addWarningComment(warning_id){
    addComment("warning", warning_id);
}


function addComment(type, id){
    var commentField = $("#"+type+"-comment-field-"+id);
    $.post("/lanapp/"+type+"-comment/" + id, {comment: commentField.val()})
      .done(function(data) {
          updateListGrandchild(type+"-comment", id)
      });
}

// function addContentComment(contract_id){
//     var commentField = $("#content-comment-field-"+contract_id);
//     $.post("/lanapp/content/" + contract_id, {comment: commentField.val()})
//       .done(function(data) {
//           updateListChild("content", contract_id)
//       });
// }
//
// function addWarningComment(contract_id){
//     var commentField = $("#warning-field-"+contract_id);
//     $.post("/lanapp/warning/" + contract_id, {comment: commentField.val()})
//       .done(function(data) {
//           updateListChild("warning",contract_id)
//       });
// }


function updateAllChildren(contract_id){
    updateListGrandchild("contract-comment",contract_id);
    updateListChild("content",contract_id);
    updateListChild("warning",contract_id);
}


function updateListChild(type, id) {
    var list = $("#"+type+"-list-" + id);
    // console.log('hahahha');
    // console.log(list);
    var max_time = list.data("max-time");
    // console.log(max_time);
    $.get("/lanapp/get-"+type+"s-changes/" + id + "/" + max_time)
      .done(function(data) {
          list.data('max-time', data['max-time']);
          // console.log('hahahha');
          // console.log(data.comments);
          for (var i = 0; i < data.items.length; i++) {
              var item = data.items[i];
              var new_item = $(item.html);
              list.append(new_item);

              updateListGrandchild(type+"-comment", item.id)
          }
      });
}

function updateListGrandchild(type, id){
    var list = $("#"+type+"-list-" + id);
    var max_time = list.data("max-time");
    $.get("/lanapp/get-"+type+"s-changes/" + id + "/" + max_time)
      .done(function(data) {
          list.data('max-time', data['max-time']);
          for (var i = 0; i < data.items.length; i++) {
              var item = data.items[i];
              var new_item = $(item.html);
              list.append(new_item);
          }
      });
}


function getUpdates() {
    var list = $("#contract-list");
    var max_time = list.data("max-time");
    $.get("/lanapp/get-changes/" + max_time)
      .done(function(data) {
          list.data('max-time', data['max-time']);
          for (var i = 0; i < data.contracts.length; i++) {
              var contract = data.contracts[i];
              var new_contract = $(contract.html);
              new_contract.data("contract-id", contract.id);
              // console.log('hahahha');
              // console.log(list.children());
              list.prepend(new_contract);
          }

          //update all comments
          var contracts = list.children();
          for (var j = 0; j < contracts.length; j++) {
              contract = contracts[j];

              //get the digit of id
              var idx = contract.id.lastIndexOf('-');
              updateAllChildren(contract.id.substr(idx+1))
          }
      });
}


$(document).ready(function () {
  // Add event-handlers
  // $("#contract-button").click(uploadContract);

  // Set up to-do list with initial DB items and DOM data
  populateList();

  // Periodically refresh to-do list
  // window.setInterval(getUpdates, 5000);

  // CSRF set-up copied from Django docs
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
});



// function uploadContract(){
//     var contractField = $("#contract-field");
//     $.post("/lanapp/contract-upload", {contract: contractField.val()})
//       .done(function(data) {
//           getUpdates();
//       });
// }