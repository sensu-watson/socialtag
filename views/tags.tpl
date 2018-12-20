<!DOCTYPE html>
<html lang="ja">
	<head>
		<title>社会問題タグ一覧</title>
	</head>
	<body>
		<h1>社会問題タグ一覧</h1>

		
		<ul>
			% for i in range(len(tags_array)):
			%   if count_array[i] == 0:
			%     continue
				<li><a href="/socprob/{{tags_array[i]}}">{{tags_array[i]}}({{count_array[i]}})</a></li>
			%	end
		</ul>

	</body>
</html>
