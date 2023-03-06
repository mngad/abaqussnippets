const files = [
  {name: "File 1", url: "markdown/Abaqus Material Properties.md"},

];

const container = document.getElementById("markdown-container");
const converter = new showdown.Converter();

files.forEach(file => {
  const xhr = new XMLHttpRequest();
  xhr.open("GET", file.url, true);
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {
      const markdown = xhr.responseText;
      const html = converter.makeHtml(markdown);
      const header = document.createElement("h2");
      header.textContent = file.name;
      const div = document.createElement("div");
      div.innerHTML = html;
      container.appendChild(header);
      container.appendChild(div);
    }
  };
  xhr.send();
});
