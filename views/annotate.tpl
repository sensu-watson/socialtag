<!DOCTYPE html>
<html lang="ja">
	<head>
		<title>社会問題タグ付けフォーム</title>
	</head>
	<body>
		<h1>社会問題タグ付けフォーム</h1>
		
		<form method="POST" action="/annotate">
			付与タグ <input size="100" type="search" name="tag" list="datas">
			<br>
			付与対象ページID <input size="100" type="text" name="annotate">
			<br>
			<input type="submit" value="送信">
		</form>
		
		
		<datalist id="datas">
			% for i in range(len(tags_array)):
			  <option value="{{tags_array[i]}}">{{labels_array[i]}}</option>
			% end
		</datalist>

	</body>
</html>
