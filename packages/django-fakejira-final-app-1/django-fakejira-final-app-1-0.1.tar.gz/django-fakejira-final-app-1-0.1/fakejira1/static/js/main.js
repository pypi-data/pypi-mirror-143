let scheduled_function = false; 
const delay_by_in_ms = 500;
const endpoint = '/shippings/';
const i_endpoint = '/manage-users/';

const shippings_div = $('.shipping-results');
const users_div = $('.users-results');

let filtering_shippings = function (endpoint, request_parameters) {
  $.getJSON(endpoint, request_parameters)
      .done(response => {  
        shippings_div.html(response['html_from_view']) 
        shippings_div.fadeTo('fast', 1)
      })
}

let filtering_users = function (i_endpoint, request_parameters) {
  $.getJSON(i_endpoint, request_parameters)
      .done(response => {  
        users_div.html(response['html_from_view']) 
        users_div.fadeTo('fast', 1)
      })
}
$(document).on('keyup change', '#search-shippings', function(event){ 
  event.preventDefault();
  var q = $('#search-shippings').val();
  console.log(q)
  const request_parameters = {
    q: q,
  }

  if (!$(q)) {
    q = '';
  }
  
  const nextURL = '/shippings/?q=' + q;
  const nextTitle = 'My new page url';
  const nextState = { additionalInformation: 'Updated the URL with JS' };

  window.history.pushState(nextState, nextTitle, nextURL); 

  if (scheduled_function) {
      clearTimeout(scheduled_function)
  } 
  scheduled_function = setTimeout(filtering_shippings, delay_by_in_ms, endpoint, request_parameters)
}) 

$(document).on('keyup change', '#search-users', function(event){ 
  event.preventDefault();
  var q = $('#search-users').val();
  console.log(q)
  const request_parameters = {
    q: q,
  }

  if (!$(q)) {
    q = '';
  }
  
  const nextURL = '/manage-users/?q=' + q;
  const nextTitle = 'My new page url';
  const nextState = { additionalInformation: 'Updated the URL with JS' };

  window.history.pushState(nextState, nextTitle, nextURL); 

  if (scheduled_function) {
      clearTimeout(scheduled_function)
  } 
  scheduled_function = setTimeout(filtering_users, delay_by_in_ms, i_endpoint, request_parameters)
}) 

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function CustomAlert(){
  this.alert = function(message,title){
    document.body.innerHTML = document.body.innerHTML + '<div id="dialogoverlay"></div><div id="dialogbox" class="slit-in-vertical"><div><div id="dialogboxhead"></div><div id="dialogboxbody"></div><div id="dialogboxfoot"></div></div></div>';

    let dialogoverlay = document.getElementById('dialogoverlay');
    let dialogbox = document.getElementById('dialogbox');
    
    let winH = window.innerHeight;
    dialogoverlay.style.height = winH+"px";
    
    dialogbox.style.top = "100px";

    dialogoverlay.style.display = "block";
    dialogbox.style.display = "block";
    
    document.getElementById('dialogboxhead').style.display = 'block';

    if(typeof title === 'undefined') {
      document.getElementById('dialogboxhead').style.display = 'none';
    } else {
      document.getElementById('dialogboxhead').innerHTML = '<i class="fa fa-exclamation-circle" aria-hidden="true"></i> '+ title;
    }
    document.getElementById('dialogboxbody').innerHTML = message;
    document.getElementById('dialogboxfoot').innerHTML = '<button class="pure-material-button-contained active" onclick="customAlert.ok()">OK</button>';
  }
  
  this.ok = function(){
    document.getElementById('dialogbox').style.display = "none";
    document.getElementById('dialogoverlay').style.display = "none";
  }
}

let customAlert = new CustomAlert();

$(document).on('submit', '#add-new-shipping', function(event){
  event.preventDefault(); 
  var formData = new FormData($(this)[0]);

  var product = $("input[name='product']").map(function() {
    return $(this).val();
  }).get();  

  formData.append('product', product);

  var customer = $("input[name='customer']").map(function() {
    return $(this).val();
  }).get();  

  formData.append('customer', customer);
  
  var shipping_status = $("select[name='shipping_status']").map(function() {
    return $(this).val();
  }).get();  

  formData.append('shipping_status', shipping_status);
  
  // Add csrf token
  formData.append('csrfmiddlewaretoken', csrftoken);

  $.ajax({
    type: 'POST',
    url: '/add_new_shipping/',
    data: formData,
    dataType: 'json',
    cache: false,
    processData: false,
    contentType: false,
    success: function(response){
      $('#add-new-shipping').html(response['form']);
      window.location.href = "/shippings/";
    },
    error: function(data){ 
      customAlert.alert(data.responseJSON.error)
    },
  }); 
});

$(document).on('submit', '#update-shipping-form', function(event){
  event.preventDefault(); 
  var formData = new FormData($(this)[0]);

  var product = $("input[name='product']").map(function() {
    return $(this).val();
  }).get();  

  formData.append('product', product);

  var customer = $("input[name='customer']").map(function() {
    return $(this).val();
  }).get();  

  formData.append('customer', customer);
  
  var shipping_status = $("select[name='shipping_status']").map(function() {
    return $(this).val();
  }).get();  

  formData.append('shipping_status', shipping_status);
  
  // Add csrf token
  formData.append('csrfmiddlewaretoken', csrftoken);

  $.ajax({
    type: 'POST',
    url: '/update_shipping/'+$(this).data('id') + '/',
    data: formData,
    dataType: 'json',
    cache: false,
    processData: false,
    contentType: false,
    success: function(response){
      $('#update-shipping-form').html(response['form']);
      $( "div.success" ).fadeIn( 300 ).delay( 1500 ).fadeOut( 400 );
    },
    error: function(data){ 
      customAlert.alert(data.responseJSON.error);
    },
  }); 
});

$(document).on('click', 'form .del-btn', function(event){
  event.preventDefault(); 

  $.ajax({
    type: 'POST',
    url: '/delete_shipping/'+$(this).data('id') + '/',
    data: {'csrfmiddlewaretoken':csrftoken},
    dataType: 'json',
    success: function(response){
      window.location.href = "/shippings/";
    },
    error: function(data){ 
      customAlert.alert(data.responseJSON.error);
    },
  }); 
});

$(document).on("change", '#select-all',function(){ 
  $(".checklist-item").prop('checked', $(this).prop("checked"));
  if ($('.checklist-item:checked').length == $('.checklist-item').length ){
    $('.remove-btn-section').css('display', 'block');
  }
  else {
    $('.remove-btn-section').css('display', 'none')
  }
});

$(document).on("change", '.checklist-item',function(){
  if ($('.checklist-item:checked').length) {
    $('.remove-btn-section').css('display', 'block');
  }
  else {
    $('.remove-btn-section').css('display', 'none');
  }
});

$(document).on("change", '.checklist-item',function() { 
  if (false == $(this).prop("checked")){ 
    $("#select-all").prop('checked', false) 
  } 
  if ($('.checklist-item:checked').length == $('.checklist-item').length ){
    $("#select-all").prop('checked', true);
  }
});

$(document).on('click', '.remove-btn-section .del-btn', function(event){
    event.preventDefault(); 
    
    var selected_products = $(".checklist-item:checked").map(function() {
        return $(this).attr("value");
    }).get(); 
    var products = [];

    for (var i = 0; i < selected_products.length; i++) { 
        products.push(selected_products[i]);
    }

    console.log(products)
    
    $.ajax({
        type: 'POST',
        url: '/bulk_delete_shippings/',
        data: {
            'csrfmiddlewaretoken': csrftoken,
            'products[]': products,
        },
        dataType: 'json',
        success: function(response){ 
            window.location.href = "/shippings/";
        },
        error: function(rs, e){
            customAlert.alert(data.responseJSON.error);
        },
    });
});

$(document).on('submit', '#login-form', function(event){
    event.preventDefault();

    var username = $('input[name="username"]').val();
    var password = $('input[name="password"]').val();

    $.ajax({
        type: 'POST',
        url: '/singin/',
        data: {
            'username': username,
            'password': password,
            'csrfmiddlewaretoken': csrftoken
        },
        dataType: 'json',
        success: function(response){
            $('#login-form').html(response['form']);
            window.location.href = "/shippings/";
            console.log($('#login-form').html(response['form']));
        },
        error: function(data){
            customAlert.alert(data.responseJSON.error);
        },
    });
});
