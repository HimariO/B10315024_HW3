#### B10315024_HW1
RSA.py has implemnt
+ RSA decrypt/encrypt
+ CRT fast decrypt
+ Square-Multiply
+ variable length key
+ Large prime generation(using Miller-Rabin)
+ Miller-Rabin Algorithm

Run example input by enter command:
```
python3 main.py
```
Output will look like:
```
RSA Init...
Got p
Got q
Got e
Got d
encrypted:  359546124471575764925622830273112129636688611617263683205958275104168847353351657002798266852535074050435975887995385426521413903660527829
decrypted:  123456789

```
Running example with key length under 2048bit take reasonable time, 4096bit key will take much much longer.
