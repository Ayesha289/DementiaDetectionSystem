var current_fs, next_fs, previous_fs;
var left, opacity, scale;
var animating;
$(".next").click(function () {
  if (animating) return false;
  animating = true;

  current_fs = $(this).parent();
  next_fs = $(this).parent().next();
  $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
  next_fs.show();
  current_fs.animate(
    { opacity: 0 },
    {
      step: function (now, mx) {
        scale = 1 - (1 - now) * 0.2;
        left = now * 50 + "%";
        opacity = 1 - now;
        current_fs.css({
          transform: "scale(" + scale + ")",
          position: "absolute",
        });
        next_fs.css({ left: left, opacity: opacity });
      },
      duration: 800,
      complete: function () {
        current_fs.hide();
        animating = false;
      },
      easing: "easeInOutBack",
    }
  );
});

$(".previous").click(function () {
  if (animating) return false;
  animating = true;

  current_fs = $(this).parent();
  previous_fs = $(this).parent().prev();
  $("#progressbar li")
    .eq($("fieldset").index(current_fs))
    .removeClass("active");

  previous_fs.show();
  current_fs.animate(
    { opacity: 0 },
    {
      step: function (now, mx) {
        scale = 0.8 + (1 - now) * 0.2;
        left = (1 - now) * 50 + "%";
        opacity = 1 - now;
        current_fs.css({ left: left });
        previous_fs.css({
          transform: "scale(" + scale + ")",
          opacity: opacity,
        });
      },
      duration: 800,
      complete: function () {
        current_fs.hide();
        animating = false;
      },
      easing: "easeInOutBack",
    }
  );
});
const genderInput = document.getElementById("gender");

genderInput.addEventListener("keyup", function() {
  const value = this.value.toLowerCase();
  if (value === "m" || value === "f") {
    this.style.border = "1px solid green";
  } else {
    this.style.border = "1px solid red";
  }
});
function validateAge(inputField) {
  const value = inputField.value;
  const age = parseInt(value.replace(/\D/g, ""), 10);
  if (isNaN(age) || age < 0 || age > 80) {
    inputField.style.border = "1px solid red"; 
  } else {
    inputField.style.border = "1px solid green"; 
  }
}

function validateEducationYears(inputField) {
  const value = inputField.value;
  const educationYearsInput = parseInt(value.replace(/\D/g, ""), 10);
  if (isNaN(educationYearsInput) || educationYearsInput < 0 || educationYearsInput > 30) {
    inputField.style.border = "1px solid red";
  } else {
    inputField.style.border = "1px solid green"; 
  }
}

function validateSocioStat(inputField) {
  const value = inputField.value;
  const socio = parseInt(value.replace(/\D/g, ""), 10);
  if (isNaN(socio) || socio < 0 || socio > 5) {
    inputField.style.border = "1px solid red";
  } else {
    inputField.style.border = "1px solid green";
  }
}

function validateMMSEScore(inputField) {
  const value = inputField.value;
  const mmse = parseInt(value.replace(/\D/g, ""), 10);
  if (isNaN(mmse) || mmse < 0 || mmse > 30) {
    inputField.style.border = "1px solid red";
  } else {
    inputField.style.border = "1px solid green"; 
  }
}

function validateCDR(inputField) {
  const value = inputField.value;
  const cdr = parseFloat(value);
  if (isNaN(cdr) || cdr < 0.0 || cdr > 2.0) {
    inputField.style.border = "1px solid red";
  } else {
    inputField.style.border = "1px solid green"; 
  }
}

function validateNWBV(inputField) {
  const value = inputField.value;
  const nwbv = parseFloat(value);
  if (isNaN(nwbv) || nwbv < 0.0 || nwbv > 1.0) {
    inputField.style.border = "1px solid red";
  } else {
    inputField.style.border = "1px solid green"; 
  }
}
function validateasf(inputField) {
  const value = inputField.value;
  const asf = parseFloat(value);
  if (isNaN(asf) || asf < 0.0 || asf > 2.0) {
    inputField.style.border = "1px solid red"; 
  } else {
    inputField.style.border = "1px solid green";
  }
}