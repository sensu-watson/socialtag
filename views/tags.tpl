<!DOCTYPE html>
<html lang="ja">
	<head>
		<title>社会問題タグ一覧</title>
	</head>
	<body>
		<h1>社会問題タグ一覧</h1>

		
		<ul>
			% for tag in tags_array:
				<li><a href="/socprob/{{tag}}">{{tag}}</a></li>
			%	end
		</ul>

	</body>
</html>
