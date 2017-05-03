 --init.lua
 gpio = 3
 require('ds18b20')
 ds18b20.setup(gpio)
 wifi.setmode(wifi.STATION)
 wifi.sta.config("x1","pass")
 wifi.sta.connect()
 tmr.alarm(1, 1000, 1, function()
  if wifi.sta.getip()== nil then
  print("IP unavaiable, Waiting...")
 else
  tmr.stop(1)
 print("ESP8266 mode is: " .. wifi.getmode())
 print("The module MAC address is: " .. wifi.ap.getmac())
 print("Config done, IP is "..wifi.sta.getip())
 end
 end)
 
 local function measureTemp()
    local temp
    repeat temp = ds18b20.read() until temp ~= 85
    return temp
  end
 
 
srv=net.createServer(net.TCP)

srv:listen(80,function(conn)
    conn:on("receive", function(client,request)
		t=measureTemp()
				
		print("Temp:"..t.." C\n")
        local buf = "HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n"
        
        buf = buf.."<h1>ESP8266 Web Server</h1>";
		buf = buf.."<p>temp:"..t.."C</p>";
        
        
        client:send(buf);
        client:close();
        collectgarbage();
    end)
end)