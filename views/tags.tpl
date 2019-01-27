<!DOCTYPE html>
<html lang="ja">
	<head>
		<title>タグ一覧</title>
	</head>
	<body>
		<h1>タグ一覧</h1>
		
		<h2>社会問題タグ</h2>
		<ul>
			% for i in range(len(social_tags_array)):
			%   if social_count_array[i] == "0":
			%     continue
			%   else:
			<li><a href="/socprob/{{social_labels_array[i]}}">{{social_labels_array[i]}}({{social_count_array[i]}})</a></li>
			%   end
			%	end
		</ul>
		
		
		<h2>その他タグ</h2>
		<ul>
			% for i in range(len(other_tags_array)):
			%   if other_count_array[i] == "0":
			%     continue
			%   else:
			<li><a href="/other/{{other_labels_array[i]}}">{{other_labels_array[i]}}({{other_count_array[i]}})</a></li>
			%   end
			%	end
		</ul>

	</body>
</html>
