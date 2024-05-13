#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 10:30:56 2024

@author: chiarafischer
"""

import math


class Solution(object):
    
    # find median of two sorted arrays
    def findMedianSortedArrays(self, nums1, nums2):
        merged_array = []
        all_elements = len(nums1) + len(nums2)
        counter_nums1 = 0
        counter_nums2 = 0

        while(all_elements > 0) :
            if(counter_nums1 >= len(nums1)) :
                merged_array.append(nums2[counter_nums2])
                counter_nums2 += 1
            elif(counter_nums2 >= len(nums2)) :
                merged_array.append(nums1[counter_nums1])
                counter_nums1 += 1
            elif(nums1[counter_nums1] < nums2[counter_nums2]):
                merged_array.append(nums1[counter_nums1])
                counter_nums1 += 1
            else :
                merged_array.append(nums2[counter_nums2])
                counter_nums2 += 1
            
            all_elements -= 1
        

        if(all_elements % 2 == 0) :
            result = (merged_array[math.trunc(all_elements / 2)] + merged_array[math.trunc(all_elements / 2 - 1)])/2
        else :      
            result = merged_array[math.trunc(all_elements / 2)]
        

        return(result)


    # find median of two lists
    def findMedianEasy(self, nums1, nums2):
        
        merged = nums1 + nums2
        merged.sort()
        
        if(len(merged) % 2 == 0) :
            result = (merged[math.trunc(len(merged) / 2)] + merged[math.trunc(len(merged) / 2 - 1)])/2
        else :      
            result = merged[math.trunc(len(merged) / 2)]
        

        return(result)
    
    
    # reverse an integer
    def reverseInteger(self, x):
        array_ints = str(x)
        rev = ""
        for i in range(len(array_ints)-1, -1, -1): # in range, it does exlcude the last element, therefore until -1 instead of 0
            rev = rev + (array_ints[i])
    
        return(int(rev))
    
    
    # This function calculates the maximum area between vertical lines and the x-axis, given a list of heights of the lines
    def maxArea(self, height):
        maxVol = 0
        for i in range(0, len(height) - 1):
            for j in range(i+1, len(height)):
                smaller_height = min(height[i], height[j])
                vol = ((j+1) - (i+1)) * abs(smaller_height)
                if(vol > maxVol):
                    maxVol = vol
    
        return(maxVol)
    

    # transform an integer into its roman numeral representation
    def intToRoman(self, num):
        final = ""
        roman = ["M", "D", "C", "L", "X", "V", "I"]
        nums = [1000,500,100,50,10,5,1]
    
        while(num > 0):
            counter = 0
            while(num < nums[counter]):
                counter = counter + 1
            print(counter)
            final = final + roman[counter]
            num = num - nums[counter] 
        
        return final


    # find longest common prefix in a list of strings
    def longestCommonPrefix(self, strs):
        words = len(strs)
        pre = ""
        counter = 0
        same = True
        if(words == 1):
            return pre
        else:
            while(same):
                new = strs[0][counter]
                for i in range(1,words):
                    if(strs[i][counter]) != new:
                        same = False
                        return pre
                if(same):
                    counter = counter + 1
                    pre = pre + new

        return (pre)
    
    
    
    # This function finds the sum of three integers in a list (nums) that is closest to a given target intege
    def threeSumClosest(self, nums, target):
        curr = nums[0] + nums[1] + nums[2] 
        
        if(len(nums) == 3):
            return curr
        else:
            for i in range(0, len(nums) - 2):
                val = nums[i]
                for j in range(i+1, len(nums) - 1):
                    val2 = val + nums[j]
                    for x in range(j+1, len(nums)):
                        val3 = val2 + nums[x]
                        if(val == target):
                            return val3
                        if(abs(val3-target) < abs(curr-target)):
                            curr = val3
        return curr
        

    # This function generates all possible letter combinations that can be formed by pressing the given digits on a phone keypad
    def letterCombinations(self, digits):
        combinations = ['']
        
        seq = {
            '2': ['a', 'b', 'c'],
            '3': ['d', 'e', 'f'],
            '4': ['g', 'h', 'i'],
            '5': ['j', 'k', 'l'],
            '6': ['m', 'n', 'o'],
            '7': ['p', 'q', 'r', 's'],
            '8': ['t', 'u', 'v'],
            '9': ['w', 'x', 'y','z']
        }

        # Iterate over each digit in the input
        for digit in digits:
            new_combinations = []
            # And append each letter belonging to that input digit to the existing combinations
            for combination in combinations:
                for letter in seq[digit]: # use values of that key
                    new_combinations.append(combination + letter)
            combinations = new_combinations
        return combinations
    
    
    
    
    # check whether order of parenthesisis valid
    def isValid(self, s):
        stack = []
        openP = ['(', '{', '[']
        closeP = [')', ']', '}']
    
        for i in s:
            if(i in openP):
                stack.append(i)
                print("Adding")
            else:
                if(len(stack) == 0):
                    return False
                else:
            
                    get_Element_to_pop = stack[len(stack)-1]
                    if(get_Element_to_pop == '(' and i == ')') or (get_Element_to_pop == '{' and i == '}') or (get_Element_to_pop == '[' and i == ']'):
                        stack.pop()
                    else: 
                        return False
        if(len(stack) == 0):
            return True
        else:
            return False



    # This function generates all valid combinations of well-formed parentheses given the number n
    def generateParenthesis(self,n):
        results = []
        
        def recurse(sequence='', left=0, right=0):
            if len(sequence) == 2 * n: # means sequence is done
                results.append(sequence)
                return
            # if we are not done, explore two paths:
            if left < n: # we have spare open parentheses left, so we add one
                recurse(sequence + '(', left + 1, right) # increase counter of left
            if right < left: # we have more openings than closing, so we add one closing parentheses
                recurse(sequence + ')', left, right + 1)
    
        recurse()
        return results



    # This function generates all permutations of a given list of numbers nums
    def permutation(self, nums):
        results = []
        
        def recurse(sequence, remaining):
            if not remaining:  # If there are no more elements to permute
                results.append(sequence)
                return
            for i in range(len(remaining)):
                # Recurse by including the current element and excluding it from remaining list
                recurse(sequence + [remaining[i]], remaining[:i] + remaining[i+1:])
        
        recurse([], nums)
        return results
    
    
    
    # This function generates the next permutation of a list of numbers nums in lexicographic order
    def nextPermu(self, nums):
        # Find the rightmost ascent where nums[i] < nums[i + 1]
        i = len(nums) - 2
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1
    
        # If there was no ascent, the array is the highest permutation
        if i == -1:
            nums.reverse()
            return
        
        # Find the smallest element on the right of the ascent that is larger than nums[i]
        j = len(nums) - 1
        while nums[j] <= nums[i]:
            j -= 1
        
        # Swap the two elements
        nums[i], nums[j] = nums[j], nums[i]
        
        # Reverse the part of the array after i to get the lowest lexicographical order starting from i+1
        nums[i + 1:] = reversed(nums[i + 1:])
        
        
    # This function is meant to find the range of indices where a target element appears in a sorted list of numbers nums
    def searchRange(self, nums, target):
        res = [-1, -1]
        changed = False
        last = -1
    
        for i in range(0,len(nums)): 
            if nums[i] == target and not changed:  # Using 'and' instead of '&', also simplified condition
                changed = True
                res[0] = i
                last = i
            elif nums[i] == target and changed:  # Using 'and' instead of '&', also simplified condition
                last = i
            elif nums[i] != target and changed:  # Using 'and' instead of '&', also simplified condition
                res[1] = last
    
        if changed and res[1] == -1:  # Using 'and' instead of '&'
            res[1] = len(nums)-1
            
        return res


    # check whether a sodoku board (including entries) is valid of whether mistakes were made
    def isValidSudoku(self, board):

        new_box = {0,3,6}
        
        # first for rows and columns
        for i in range(0,9):
            values_row = set()
            values_column = set()
            box = set()

            for j in range(0,9):
                if(i in new_box and j in new_box):
                    box = set() # overwrite
                
                if(board[i][j] in values_row and board[i][j] != "." or board[j][i] in values_column and board[j][i] != "." or board[i][j] in box and board[i][j] != "."):
                    return False
                else:
                    values_row.add(board[i][j])
                    values_column.add(board[j][i])
                    box.add(board[i][j])
        
        return True
         
        


# Test Cases

obj = Solution()
#res = obj.findMedianSortedArrays([1,2], [3,4])
#res2 = obj.findMedianEasy([1,2], [3,4])
#rev = obj.reverseInteger(123)
#split = obj.getChars("hallo")
#split.reverse() # returns the original list and returns none
#rom = obj.intToRoman(3)
#pre = obj.longestCommonPrefix(["hallo", "hi"])
#s = obj.threeSumClosest([1,1,1,1], 100)
#b = obj.isValid("()")
#paren = obj.generateParenthesis(2)
#permu = obj.permutation([1,2,3])
#l = [5,7,7,8,8,10]
#range = obj.searchRange(l,8)
#valid = obj.isValidSudoku([["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]])














