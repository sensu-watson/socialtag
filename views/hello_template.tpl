<!DOCTYPE html>
<html lang="ja">
	<head>
		<title>社会問題タグ付けフォーム</title>
	</head>
	<body>
		<h1>社会問題タグ付けフォーム</h1>
		
		<form method="POST" action="/">
			付与タグ <input type="search" name="tag" list="datas">
			<br>
			付与対象ページ <input type="text" name="annotate">
			<br>
			付与者email <input type="text" name="email">
			<br>
			<input type="submit" value="送信">
		</form>
		
		
		<datalist id="datas"></datalist>

		<script>
			let query = 'select ?uri, ?label where{'
					+ '?uri <https://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Class>.'
					+ '?uri <http://www.w3.org/2000/01/rdf-schema#label> ?label.'
					+ '}'
			let format = 'application/sparql-results+json'
			let graphuri = 'http://lod.srmt.nitech.ac.jp/socprob/'


			let url = 'http://lod.srmt.nitech.ac.jp/sparql/'

			url = url + '?' + 'default-graph-uri=' + encodeURIComponent(graphuri) + '&query=' + encodeURIComponent(query) + '&format=' + encodeURIComponent(format)

			fetch(url, {
  			method: 'GET'
			}).then(res => {
				
				res.text().then(text => {
					let results = JSON.parse(text);
					let bindings = results['results']['bindings'];
					
					const datas = document.getElementById('datas');
					for (let x of bindings){
						let uri = x['uri']['value'];
						let label = x['label']['value'];

						let node = document.createElement("option");
						let value = document.createAttribute("value");
  					value.nodeValue = uri;
  					node.setAttributeNode(value);

						let text = document.createTextNode(label);
						node.appendChild(text);

						datas.appendChild(node);
					}
					
				});
   			
			}).catch(err => console.error(err));
		</script>
	</body>
</html>
