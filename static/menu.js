let currentOperation = "";

function clearInputs() {
  document.getElementById('input1').value = '';
  document.getElementById('input2').value = '';
  document.getElementById('result').value = '';
  currentOperation = "";
}

async function submitData(operation) {
  currentOperation = operation;

  const val1 = document.getElementById('input1').value;
  const val2 = document.getElementById('input2').value;
  const resultBox = document.getElementById('result');

  if(["factorial", "fibonacci", "sqrt"].includes(currentOperation)) {
    if(!isValidInteger(val1)) {
      resultBox.value = "Error: Input must be an integer";
      return;
    }
    else if(val2 !== '') {
      resultBox.value = "Error: Too many arguments";
      return;
    }
  }

  if(["logarithm", "power"].includes(currentOperation)) {
    if(!isValidInteger(val1) || !isValidInteger(val2)) {
      resultBox.value = "Error: Inputs must be integers";
      return;
    }
  }

  let url = "";
  let numbers = {};

  switch(currentOperation) {
    case "factorial":
      url = "/factorial";
      numbers = {n: parseInt(val1)};
      break;
    case "fibonacci":
      url = "/fibonacci";
      numbers = {n: parseInt(val1)};
      break;
    case "logarithm":
      url = "/log";
      numbers = {n: parseInt(val1), base: parseInt(val2)};
      break;
    case "power":
      url = "/pow";
      numbers = {base: parseInt(val1), exponent: parseInt(val2)};
      break;
    case "sqrt":
      url = "/sqrt";
      numbers = {n: parseInt(val1)};
      break;
    default:
      resultBox.value = "Invalid operation";
      return;
  }

  try {
    const res = await fetch(url, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(numbers)
    });

    if(!res.ok) {
      const err = await res.json();
      if(err.detail) {
        const message = Array.isArray(err.detail) ? err.detail[0].msg : err.detail;
        resultBox.value = `Error: ${message}`;
      } else {
        resultBox.value = "Unknown error occurred.";
      }
    }

    const data = await res.json();
    resultBox.value = data.result;
  } catch(err) {
    console.log(err);
  }
}

function isValidInteger(value) {
  if(value === "") return false;
  const parsed = Number(value);
  return Number.isInteger(parsed) && !isNaN(parsed);
}

async function getUserInfo() {
  try {
      const res = await fetch("/userinfo", {
        method: "GET",
        credentials: "include"
      });
      if (res.ok) {
          const data = await res.json();
          document.getElementById("username").innerText = data.username;
      } else {
          window.location.href = "/";
      }
  } catch (err) {
      console.error("User info fetch failed", err);
      window.location.href = "/";
  }
}

function logout() {
    document.cookie = "access_token=; path=/; Max-Age=0;";
    channel.postMessage('logout');
    window.location.href = "/logout";
}

getUserInfo();