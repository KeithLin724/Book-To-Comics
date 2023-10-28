$(document).ready(() => {
  document.getElementById("messageArea").addEventListener("submit", (event) => {
    const date = new Date();
    const hour = date.getHours();
    const minute = date.getMinutes();
    const str_time = hour + ":" + minute;
    var textInput = document.getElementById("text");
    var rawText = textInput.value;

    var userHtml =
      '<div class="d-flex justify-content-end mb-4"><div class="msg_cotainer_send">' +
      rawText +
      '<span class="msg_time_send">' +
      str_time +
      '</span></div><div class="img_cont_msg"><img src="https://i.ibb.co/d5b84Xw/Untitled-design.png" class="rounded-circle user_img_msg"></div></div>';

    textInput.value = "";

    document.getElementById("messageFormeight").innerHTML += userHtml;

    var sendData = {
      msg: rawText,
    };

    var requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(sendData),
    };

    console.log(requestOptions);

    fetch("/get", requestOptions)
      .then((response) => response.json())
      .then((recvData) => {
        // console.log(recvData); // type is json
        console.log(recvData["msg"]);
        var botHtml =
          '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="https://i.ibb.co/fSNP7Rz/icons8-chatgpt-512.png" class="rounded-circle user_img_msg"></div><div class="msg_cotainer">' +
          recvData["msg"] +
          '<span class="msg_time">' +
          str_time +
          "</span></div></div>";
        document
          .getElementById("messageFormeight")
          .insertAdjacentHTML("beforeend", botHtml);
      })
      .catch((error) => {
        console.error("Error:", error);
      });

    event.preventDefault();
  });
});
