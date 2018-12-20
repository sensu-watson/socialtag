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
		
		
		<datalist id="datas">
			% for tag in tags_array:
			  <option value="http://tag.srmt.nitech.ac.jp/socprob/{{tag}}">{{tag}}</option>
			% end
		</datalist>

	</body>
</html>
