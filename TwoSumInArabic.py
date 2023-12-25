عين TwoSum( nums, target ):
	h = {}
	لهذا i في نطاق(طول(nums)):
		diff = target - nums[i]
		إذا diff في h: رجع [h[diff], i]
		اخر: h[nums[i]] = i

testcases = [
	[[2,7,11,15], 9], # -> [0, 1]
	[[2,7,11,15], 26], # -> [2, 3]
	[[99, 1, 123], 100], # -> [0, 1]
	[[1, 2, 3, 4, 5, 6], 10], # -> [3, 5]
	[[0, 0, 0, 0, 0, 1], 1], # -> [4, 5]
	[[-1, 1, 0, 6], 6] # -> [2, 3]
]

لهذا nums, target في testcases:
	اطبع(TwoSum(nums, target))