
def is_phrase_in(text, phrase):
	import string 
	new_text = ''
	for chars in text:
		if chars in string.punctuation:
			new_text += chars.replace(chars, ' ')
		else:
			new_text += chars 
	lower_string = new_text.lower			
	text_list = new_text.split(' ')
	new_list = list(filter(None, text_list))
	lower_p = phrase.lower()	
	phrase_list = lower_p.split(' ')
	#i for i in new_list if i in phrase_list
	# s = ' ' 
	# parsed_string = s.join(new_list)
	# if phrase in parsed_string:
		# #return True 
		# print('True')
	# else:
		# #return False
		# print('False')
	
	
	
	
	
is_phrase_in('The purple cow is soft and cuddly', 'purple cow')
#we need to now remove extra spaces in the sentence
#make sure that new_text is all lower case as well 