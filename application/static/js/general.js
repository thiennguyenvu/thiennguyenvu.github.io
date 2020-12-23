function loadFileServer(filePath) {
  var result = null;
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("GET", filePath, false);
  xmlhttp.send();
  if (xmlhttp.status == 200) {
    result = xmlhttp.responseText;
  }
  return result;
}

var _getJSON = function (url, callback) {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", url, true);
  xhr.responseType = "json";

  xhr.onload = function () {
    var status = xhr.status;

    if (status == 200) {
      callback(null, xhr.response);
    } else {
      callback(status);
    }
  };
  xhr.send();
};

function uniq_arr(arr) {
  var seen = {};
  var out = [];
  var len = arr.length;
  var j = 0;
  for (var i = 0; i < len; i++) {
    var item = arr[i];
    if (seen[item] !== 1) {
      seen[item] = 1;
      out[j++] = item;
    }
  }
  return out;
}

function getDataModel(url, i_col, i_row, result) {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", url, true);
  xhr.responseType = "arraybuffer";
  xhr.onload = function (evt) {
    var data = new Uint8Array(xhr.response);
    var workbook = XLSX.read(data, { type: "array" });
    var sheet = workbook.Sheets[workbook.SheetNames[0]];
    var range = XLSX.utils.decode_range(sheet["!ref"]);

    //result.push(""); // empty index 0
    // range.e.r = range.end.row
    for (row = 1; row <= range.e.r + 1; row++) {
      if (i_col === 1) {
        var col_model = "A" + i_row;
        if (sheet[col_model] !== undefined) {
          return sheet[col_model].v;
        } else {
          return "";
        }
      }
      if (i_col === 2) {
        var col_arm = "B" + row;
        if (sheet[col_arm] !== undefined) {
          return sheet[col_arm].v;
        } else {
          return "";
        }
      }
      if (i_col === 3) {
        var col_ass = "C" + row;
        if (sheet[col_ass] !== undefined) {
          return sheet[col_ass].v;
        } else {
          return "";
        }
      }
    }
  };
  xhr.send();
}

function getExcelData_Model(url, arr) {
  var req = new XMLHttpRequest();
  req.open("GET", url, true);
  req.responseType = "arraybuffer";

  req.onload = function (e) {
    var data = new Uint8Array(req.response);
    var workbook = XLSX.read(data, { type: "array" });
    var sheet = workbook.Sheets[workbook.SheetNames[0]];
    var range = XLSX.utils.decode_range(sheet["!ref"]);
    var model = [],
      arm = [],
      ass = [];
    model.push(""), arm.push(""), ass.push(""); // empty index 0
    // range.e.r = range.end.row
    for (row = 1; row <= range.e.r + 1; row++) {
      var col_model = "A" + row;
      var col_arm = "B" + row;
      var col_ass = "C" + row;
      if (sheet[col_model] !== undefined) {
        model.push(sheet[col_model].v);
      } else {
        model.push("");
      }
      if (sheet[col_arm] !== undefined) {
        arm.push(sheet[col_arm].v);
      } else {
        arm.push("");
      }
      if (sheet[col_ass] !== undefined) {
        ass.push(sheet[col_ass].v);
      } else {
        ass.push("");
      }
    }
    arr.push(model, arm, ass);
    console.log(model, arm, ass);
  };
  req.send();
}
