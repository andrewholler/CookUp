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
  el.id = "search-result-list"
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
      li.id = opt.ndbno;
      el.appendChild(li);
  }
}

function addIngredient(element) {
  // Add an ingredient to the ingredient list
  var list = document.getElementById("ingredient-list");
  
  // Add the quantity input
  var div = document.createElement("div");
  div.className = "col-lg-2";
  list.appendChild(div);
  var input = document.createElement("input");
  input.type = "number";
  input.value = 0;
  input.min = 0;
  input.className = "form-control";
  input.name = "ingredient-amount";
  input.setAttribute("onchange", "updateCalories(this);");
  div.appendChild(input);
  
  // Add the measures input
  div = document.createElement("div");
  div.className = "col-lg-2";
  list.appendChild(div);
  var select = document.createElement("select");
  select.className = "form-control";
  select.name = "ingredient-measure";
  select.form = "recipeForm";
  select.setAttribute("onchange", "updateCalories(this);");
  div.appendChild(select);
  
  var url = "https://api.nal.usda.gov/ndb/V2/reports?ndbno=" + element.currentTarget.id + "&type=b&format=json&api_key=W0hVxQq8rODeGQiB06CoDvHnhgibC6eUT9CsZjZD";
  console.log(url);
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", url, false);
  xhttp.send();
  var response = JSON.parse(xhttp.responseText);
  
  if (response.notfound) {
    console.log("Couldn't get food report for ingredient " + element.currentTarget.id);
  }
  else {
    for(var i = 0; i < response.foods[0].food.nutrients.length; i++) {
      var nutrient = response.foods[0].food.nutrients[i];
      if (nutrient.nutrient_id == "208") {
        for(var j = 0; j < nutrient.measures.length; j++) {
          var option = document.createElement("option");
          option.value = nutrient.measures[j].label;
          option.innerText = nutrient.measures[j].label;
          option.id = nutrient.measures[j].eqv;
          select.appendChild(option);
        }
      }
    }
  }
  
  // Add the ingredient
  var ingredient = document.createElement("div");
  ingredient.className = "col-sm-8";
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
  deletebutton.setAttribute("onclick", "this.parentNode.parentNode.parentNode.parentNode.removeChild(this.parentNode.parentNode.parentNode.previousSibling); this.parentNode.parentNode.parentNode.parentNode.removeChild(this.parentNode.parentNode.parentNode.previousSibling); this.parentNode.parentNode.parentNode.parentNode.removeChild(this.parentNode.parentNode.parentNode);");
  deletebutton.style = "cursor: pointer";
  span.appendChild(deletebutton);
  
  // Deletes search result list after you select an item
  select = document.getElementById("search-result-list");
  while (select.firstChild) {
    select.removeChild(select.firstChild);
  }
}

function updateCalories(element) {
  calories_box = document.getElementById("calories");
  ingredients = document.getElementById("ingredient-list");
  
  var newval = 0.0;
  for(var i = 0; i < ingredients.children.length; i += 3) {
    newval += ingredients.children[i].firstChild.value*parseFloat(ingredients.children[i+1].firstChild.selectedOptions[0].id);
  }
  calories_box.value = newval;
  
  //calories_box.value = parseFloat(calories_box.value) + (parseFloat(element.selectedOptions[0].id))*(element.parentNode.previousSibling.firstChild.value);
}
