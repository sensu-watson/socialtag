<!DOCTYPE html>
<html lang="ja">
	<head>
		<title>{{tagname}} | 社会問題タグ</title>
	</head>
	<body>
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
		
		<h2>付与されたページ</h2>
		<ul>
			% for target in target_array:
				<li><a href="{{target}}">{{target}}</li>
			%	end
		</ul>

	</body>
</html>
