import json

results = json.loads(open('check.json', 'r').read())

print(results)

best_accuracy = max([x[4] for x in results])
best_accuracy_details = [x for x in results if x[4] == best_accuracy][0]
print("BEST RESULT DETAILS")
print('Interval: ' + best_accuracy_details[0])
print('K: ' + str(best_accuracy_details[1]))
print('Coin: ' + best_accuracy_details[2])
print('Predict Coin: ' + best_accuracy_details[3])
print('Accuracy: ' + repr(best_accuracy_details[4]) + '%')
print('-------------------------')