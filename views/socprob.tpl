<!DOCTYPE html>
<html lang="ja">
	<head>
		<title>{{tagname}} | 社会問題タグ</title>
	</head>
	<body>
		<a href="/">タグ一覧</a>
		
		
		<h1>{{tagname}} | 社会問題タグ</h1>
		
		<h2>親タグ</h2>
		<ul>
			% for parent in parent_array:
		    <li><a href="/socprob/{{parent}}">{{parent}}</a></li>
			% end
		</ul>

		<h2>子タグ</h2>
		<ul>
			% for child in child_array:
		    <li><a href="/socprob/{{child}}">{{child}}</a></li>
			% end
		</ul>
		
		<h2>付与されたページ({{count}})</h2>
		<ul>
			% for i in range(len(target_array)):
				<li><a href="{{target_array[i]}}">{{name_array[i]}}</li>
			% end
		</ul>

	</body>
</html>
