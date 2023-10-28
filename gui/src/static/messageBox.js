$(document).ready(() => {
  /**
   * The function "makeRequestOptions" creates and returns an object with the necessary options for
   * making a POST request with JSON data.
   * @param sendData - The `sendData` parameter is an object that contains the data that you want to send
   * in the request body. This data will be converted to a JSON string using `JSON.stringify()` before
   * being sent in the request.
   * @returns an object containing the request options for making a POST request.
   */
  function makeRequestOptions(sendData) {
    var requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(sendData),
    };

    return requestOptions;
  }

  /**
   * The function `get_time()` returns the current hour and minute in a formatted string.
   * @returns The function `get_time()` returns the current time in the format "hour:minute".
   */
  function get_time() {
    const date = new Date();
    const hour = date.getHours();
    const minute = date.getMinutes();
    return hour + ":" + minute;
  }

  document.getElementById("messageArea").addEventListener("submit", (event) => {
    const str_time = get_time();
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
      .then((response) => {
        const contentType = response.headers.get("content-type");

        if (contentType.includes("application/json")) {
          // json headers
          return jsonHandler(response);
        } else if (contentType.includes("image/jpeg")) {
          // jpeg headers
          return imageHandler(response);
        } else {
          // Handle other content types here
          throw new Error("Unsupported content type: " + contentType);
        }
      })

      .catch((error) => {
        console.error("Error:", error);
      });

    event.preventDefault();
  });

  /**
   * The function `putMessage` is used to display a message with a timestamp in a chat interface.
   * @param displayStr - The displayStr parameter is a string that represents the message that you want
   * to display in the chat. It can be any text or HTML content that you want to show to the user.
   * @param str_time - The `str_time` parameter is a string representing the time at which the message is
   * being displayed. It is used to add a timestamp to the message.
   */
  function putMessage(displayStr, str_time) {
    var botHtml =
      '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="https://i.ibb.co/fSNP7Rz/icons8-chatgpt-512.png" class="rounded-circle user_img_msg"></div><div class="msg_cotainer">' +
      displayStr +
      '<span class="msg_time">' +
      str_time +
      "</span></div></div>";

    document
      .getElementById("messageFormeight")
      .insertAdjacentHTML("beforeend", botHtml);

    // const image = document.getElementById("image");
    // if (image !== null) {
    //   image.style.width = "200px";
    //   image.style.height = "auto";
    // }
  }

  /**
   * The function `jsonHandler` handles the response from a JSON API, retrieves a task ID, polls for the
   * result of the task, requests an image from the server based on the result, and then handles the
   * image.
   * @param response - The `response` parameter is the response object returned from a fetch request. It
   * contains information about the response, such as the status code and headers, as well as methods to
   * retrieve the response body. In this case, the `jsonHandler` function expects the response body to be
   * in JSON format.
   * @returns The function `jsonHandler` is returning a promise that resolves to the result of the
   * `imageHandler` function.
   */
  function jsonHandler(response) {
    return response.json().then((recvData) => {
      if ("task_id" in recvData) {
        console.log(`ok get it task_id : ${recvData["task_id"]}`);

        const task_result_json = pollForImageResult(recvData["task_id"])
          .then((result) => result)
          .catch((error) => {
            console.error("get image dict", error);
          });
        // console.log(task_result_json);

        const image_result = task_result_json
          .then((result) => requestServerImage(result))
          .catch((error) => {
            console.error("获取图像URL时发生错误:", error);
          });

        return image_result.then((result) => imageHandler(result));
      }
      return putMessage(recvData["msg"], get_time());
    });
  }

  /**
   * The imageHandler function takes a response object, retrieves the image blob from it, creates a URL
   * for the image blob, and returns an HTML string containing an image tag with the source set to the
   * created URL.
   * @param response - The `response` parameter is the response object returned from a fetch request. It
   * contains information about the response, such as the status code, headers, and the response body.
   * @returns The function `imageHandler` is returning a promise that resolves to the result of calling
   * the `putMessage` function with the `imageHtml` and `get_time()` as arguments.
   */
  function imageHandler(response) {
    return response.blob().then((imageBlob) => {
      const imgUrl = URL.createObjectURL(imageBlob);
      const imageHtml = `<img src="${imgUrl}" alt="Received Image" class="image_class">`;

      return putMessage(imageHtml, get_time());
    });
  }

  /**
   * The function `pollForImageResult` is a JavaScript function that polls a Flask server to check if an
   * image is ready and returns the result when it is.
   * @param taskId - The `taskId` parameter is the unique identifier for the task or job that is being
   * performed. In this case, it is used to track the progress of the image processing task.
   * @returns The function `pollForImageResult` returns a Promise.
   */
  function pollForImageResult(taskId) {
    return new Promise((resolve, reject) => {
      function checkImageStatus() {
        // 发送 GET 请求到 Flask 服务器以检查图像是否准备就绪
        fetch(`/check_image_state?task_id=${taskId}`)
          .then((response) => response.json())
          .then((data) => {
            if (data.state === "finished") {
              // 图像已准备就绪，显示或处理图像
              resolve(data.result);
            } else {
              // 图像还未准备就绪，继续轮询
              setTimeout(checkImageStatus, 1000); // 每隔1秒轮询一次
            }
          })
          .catch((error) => {
            reject(error);
          });
      }

      checkImageStatus();
    });
  }

  /**
   * The function `requestServerImage` sends a request to the server for an image and handles the
   * response based on the content type.
   * @param jsonDict - The `jsonDict` parameter is a JavaScript object that contains the data to be sent
   * to the server as JSON. It is used to make the request options for the `fetch` function.
   * @returns The function `requestServerImage` returns a Promise.
   */
  function requestServerImage(jsonDict) {
    const requestOption = makeRequestOptions(jsonDict);

    return fetch("/image-result", requestOption)
      .then((response) => {
        const contentType = response.headers.get("content-type");

        if (contentType.includes("application/json")) {
          // have error
          return response.json().then((recvData) => recvData["msg"]);
        } else if (contentType.includes("image/jpeg")) {
          // run image render
          return imageHandler(response);
        } else {
          throw new Error("Unsupported content type: " + contentType);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
});
