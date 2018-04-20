function searchIngredient() {
  var search_query = document.getElementById("thesearchbox").value;
  console.log(search_query);
  var xhttp = new XMLHttpRequest();
  var url = "https://api.nal.usda.gov/ndb/search/?format=json&q=" + search_query + "&sort=r&max=50&offset=0&api_key=W0hVxQq8rODeGQiB06CoDvHnhgibC6eUT9CsZjZD&ds=Standard%20Reference";
  console.log(url);
  xhttp.open("GET", url, false);
  //xhttp.setRequestHeader("Content-type", "application/json");
  xhttp.send();
  var response = JSON.parse(xhttp.responseText);
  console.log(response);
  
  select = document.getElementById("testing");
  
  while (select.firstChild) {
    select.removeChild(select.firstChild);
  }
  
  var el = document.createElement("ul");
  el.className = "list-group";
  select.appendChild(el);
  
  if (response.errors) {
    li = document.createElement("li")
    li.className = "list-group-item";
    li.textContent = "No results found. Try a different variation.";
    li.value = "No results found. Try a different variation.";
    el.appendChild(li);
  }

  for(var i = 0; i < response.list.item.length; i++) {
      var opt = response.list.item[i];
      var li = document.createElement("li");
      li.className = "list-group-item";
      li.textContent = opt.name;
      li.value = opt.name;
      li.style = "cursor: pointer";
      li.onclick = function(li){addIngredient(li)};
      el.appendChild(li);
  }
}

function addIngredient(element) {
  var list = document.getElementById("ingredient-list");
  
  var ingredient = document.createElement("div");
  ingredient.classname = "input-group stylish-input-group";
  list.appendChild(ingredient);
  
  var input = document.createElement("input");
  input.type = "hidden";
  input.class = "form-control";
  input.value = element.currentTarget.innerText;
  input.name = "ingredient";
  ingredient.appendChild(input);
  
  var li = document.createElement("li");
  li.className = "list-group-item";
  li.textContent = element.currentTarget.innerText;
  ingredient.append(li);
  
  var span = document.createElement("span");
  span.className = "delete-ingredient-icon";
  li.appendChild(span);
  
  var deletebutton = document.createElement("span");
  deletebutton.className = "glyphicon glyphicon-remove"
  deletebutton.setAttribute("onclick", "this.parentNode.parentNode.parentNode.parentNode.removeChild(this.parentNode.parentNode.parentNode);");
  deletebutton.style = "cursor: pointer";
  span.appendChild(deletebutton);
}