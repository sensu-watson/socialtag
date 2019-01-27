<!DOCTYPE html>
<html lang="ja">
	<head>
		<title>{{tagname}} | その他タグ</title>
	</head>
	<body>
		<a href="/">タグ一覧</a>
		
		<h1>{{tagname}} | その他タグ</h1>

		
		<h2>付与されたページ({{count}})</h2>
		<ul>
			% for i in range(len(target_array)):
				<li><a href="{{target_array[i]}}">{{name_array[i]}}</li>
			% end
		</ul>

	</body>
</html>
