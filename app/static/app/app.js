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
      el.appendChild(li);
  }
}











