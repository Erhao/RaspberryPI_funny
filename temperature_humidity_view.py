# coding = utf-8
# python version 3

import RPi.GPIO as GPIO
import time

channel = 35

def driver(channel):
	data = [0 for i in range(40)]
	j = 0

	# 等待1s越过不稳定状态
	GPIO.setmode(GPIO.BOARD)
	time.sleep(1)

	# 发送开始信号, 握手
	GPIO.setup(channel, GPIO.OUT)
	GPIO.output(channel, GPIO.LOW)

	# 主线拉低必须大于18ms, 最大30ms, 通知传感器准备数据(起始信号)
	time.sleep(0.02)

	# 结束主线低电位, 保证低电位只持续18ms ~ 30ms
	GPIO.output(channel, GPIO.HIGH)

	# 主线设置为输入口, 等待传感器的握手信号和数据信号
	GPIO.setup(channel, GPIO.IN)
	
	# 传感器把总线拉低83us
	while GPIO.input(channel) == GPIO.LOW:
		continue
	
	# 传感器再把主线拉高87us, 以响应主机起始信号 随后进入正式工作状态, 并开始发送数据
	while GPIO.input(channel) == GPIO.HIGH:
		continue

	# if GPIO.input(channel) == GPIO.HIGH:
	#	time.sleep(1)

	
	# 传感器收到主机起始信号后一次性发送40bit数据, 高位先出
	# 8bit湿度整数数据 + 8bit湿度小数数据(总是为0) + 8bit温度整数数据 + 8bit温度小数数据 + 8bit校验和
	while j < 40:
		k = 0
		
		# 每一位的起始信号都已50us低电平开始
		while GPIO.input(channel) == GPIO.LOW:
			continue

		# 每一位的数值信号, 高电平的长短决定了数据位是0还是1
		# 数据"0"的格式为: 54us低电平 + 23us~27us高电平
		# 数据"1"的格式为: 54us低电平 + 68us~74us高电平
#		if GPIO.input(channel) == GPIO.HIGH:
			# 记录高电平开始时间
#			high_start_timestamp = time.time()
#		high_stop_timestamp = 0	
#		if GPIO.input(channel) == GPIO.LOW:
#			# 记录高电平结束时间
#			high_stop_timestamp = time.time()
		
#		# 高电平持续时间*1000
#		if high_stop_timestamp:
#			high_stop_timestamp = time.time()
#		else:
#			high_duration = (high_stop_timestamp - high_start_timestamp) * 1000
#		if high_duration > 0.15:
#			data[j] = 1
#		else:
#			data[j] = 0
		while GPIO.input(channel) == GPIO.HIGH:
			k += 1
			if k > 100:
				break
		if k < 8:
			data[j] = 0
		else:
			data[j] = 1

		j += 1
#	print(data)
	return data

def compute(data):
	humidity_bit = data[0:8]# 分割数据
	humidity_point_bit = data[8:16]
	temperature_bit = data[16:24]
	temperature_point_bit = data[24:32]
	check_bit = data[32:40]
	humidity = 0
	humidity_point = 0
	temperature = 0
	temperature_point = 0
	check_sum = 0
	for i in range(8):
		humidity += humidity_bit[i] * 2 ** (7-i)
		humidity_point += humidity_point_bit[i] * 2 ** (7-i)
		temperature += temperature_bit[i] * 2 ** (7-i)
		temperature_point += temperature_point_bit[i] * 2 ** (7-i)
		check_sum += check_bit[i] * 2 ** (7-i)
	#   print(humidity, humidity, temperature, temperature_point, check_sum)
	# print('温度：%d  湿度：%d' %(temperature+temperature_point,humidity+humidity_point/10)    )
	num = humidity + humidity_point + temperature + temperature_point
	return num, check_sum, temperature, humidity

if __name__ == '__main__':
	delay = int(input("请输入数据采集间隔(不小于3)："))
	try:
		while 1:
			res_list = []
			while 1:
				if len(res_list) > 10:
					break
				res = compute(driver(channel))
				res_list.append(res)
				time.sleep(delay)
			temperature_sum = 0
			humidity_sum = 0
			# 温度有效数据的个数
			temperature_num = 0
			# 湿度有效数据的个数
			humidity_num = 0
			for res in res_list:
				if res[0] == res[1]:
					temperature_sum += res[2]
					temperature_num += 1
					humidity_sum += res[3]
					humidity_num += 1
			if temperature_num == 0 or humidity_num == 0:
				print('本次数据采集循环内没有获取到有效数据！')
				continue
			temperature_aver = temperature_sum / temperature_num
			humidity_aver = humidity_sum  / humidity_num
			print('-----数据正常----- 温度: %.2f   湿度：%.2f%%    采集周期%ds' % (temperature_aver, humidity_aver, delay*10))
	except KeyboardInterrupt:
		print('STOP BY USER')
		GPIO.cleanup()
