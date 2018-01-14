window.addEventListener('load', function () {
  function sendData() {
    var xhr = new XMLHttpRequest();
    xhr.responseType = 'json';
    var formData = new FormData(form);
    xhr.addEventListener('load', function(event) {
      var response = event.target.response;
      if (!response) {
        document.getElementById('subscribe-error').innerText = 'Please try again.';
        document.getElementById('subscribe-failed').style.display = 'block';

      } else if (response.message) {
        document.getElementById('subscribe-error').innerText = response.message;
        document.getElementById('subscribe-failed').style.display = 'block';
      } else {
        document.getElementById('subscribe-failed').style.display = 'none';
        document.getElementById('subscribe-succeeded').style.display = 'block';
        document.getElementById('subscribe-email').disabled = true;
        document.getElementById('subscribe-btn').disabled = true;
        document.getElementById('subscribe-btn').classList.add('disabled');
        document.getElementById('subscribe-btn').classList.remove('active');
      }
    });

    xhr.addEventListener('error', function(event) {
      var response = event.target.response;
      document.getElementById('subscribe-error').innerText = 'Please try again.';
        document.getElementById('subscribe-failed').style.display = 'block';
    });
    xhr.open('POST', '/api/subscribe');
    xhr.send(formData);
  }

  var form = document.getElementById('food-subscribe');

  form.addEventListener('submit', function (event) {
    event.preventDefault();

    sendData();
  });
});
