import asyncio
import utils as utl
import json

query = "How is the growth rate of India ?"
print(f"My query is : [{query}]")
print(f"Calling call_open_ai_with_st_op11111111")
anss =  asyncio.run(utl.call_open_ai_with_st_op1(query))
# json_anss = json.dumps(anss)
# print(f"AI Answered : [{json_anss}]")
print(f"AI Answered : [{anss}]")

print(f"Calling call_open_ai_with_st_op22222222")
anss =  asyncio.run(utl.call_open_ai_with_st_op2(query))
# json_anss = json.dumps(anss)
# print(f"AI Answered : [{json_anss}]")
print(f"AI Answered : [{anss}]")

print(f"Calling call_open_ai_with_st_op333333333")
anss =  asyncio.run(utl.call_open_ai_with_st_op3(query))
# json_anss = json.dumps(anss)
# print(f"AI Answered : [{json_anss}]")
print(f"AI Answered : [{anss}]")
