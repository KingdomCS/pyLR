import xlrd#导入用于读取Excel的库
import prettytable as pt#导入用于输出的库
import os
#----------------------------------------------------------------------
#从文件读入产生式规则,形成列表
production=[" "]*50#初始化产生式列表

production_filename="productions.txt"#包含文法的txt文件 文件名末尾不带s的是课本P159-160版本
"""
文件中产生式的格式为E->E+T则line76表达式末尾为-3
文件中产生式的格式为E#E+T则line76表达式末尾为-2
"""
file1 = open(production_filename)
i=1
while True:
    line = file1.readline()#按行读入产生式,每行一个
    if not line:
        break
    line=line.strip("\n")#去除行末换行符
    production[i]=line#加入产生式列表
    i+=1

#--------------------------------------------------------------------
#从文件读入终结符的替代规则
#使用  原终结符#替代终结符  的格式将原终结符换为仅一个字符长度
Mapdict={} #使用字典保存替代规则

map_filename="mapping.txt" #包含替代规则的txt文件

file2 = open(map_filename)

while True:
    line = file2.readline()#按行读入  原终结符#替代终结符
    if not line:
        break
    line=line.strip("\n")#去除行末换行符
    new_line=line.split("#")#使用#分割原来字符串
    orign_terminal,my_terminal=new_line[0],new_line[1]
    Mapdict[orign_terminal]=my_terminal
    
#print(Mapdict)
#---------------------------------------------------------------------
#处理输入内容,将原始的终结符使用替代规则替代
#inputstr="am=n;$"#输入内容

inputstr="const ident = number ;$"#输入内容
print("原始输入",inputstr)
str_list=inputstr[:-1].split()

new_str_list=[]
for it in str_list:
    new_str_list.append(Mapdict[it])#替换

inputstr="".join(new_str_list)
inputstr=inputstr+"$"
print("转化为简略版终结符",inputstr)
#----------------------------------------------------------------------

filename="lr.xlsx"#语法分析表文件名  lr2.xlsx是课本P159-160版本
data = xlrd.open_workbook(filename)#打开工作簿
table = data.sheets()[0]#打开表格

#table.cell_value(rowx,colx)#返回单元格中的数据

col={}#记录表头 例如:col["a"]=0
for i in range(0,43):#因为两张表表头长度不同,使用课本版本表格lr2范围是(0,9)使用标准版表格lr是(0,43)
    col[str(table.cell_value(0,i))]=i



a=inputstr[0]#输入内容的第一个符号

stack=[]#状态堆栈
stack.append(0)#压入栈底的0状态

stack_symbol=[]#符号堆栈

cnt=1

tb = pt.PrettyTable()

tb.field_names = [" ","栈", "符号", "输入", "动作"]
#下面循环中用A,B,C,D,E表示这五列

while True:
    A="("+str(cnt)+")"
    stack_new=[str(x) for x in stack]
    B=" ".join(stack_new)
    C="".join(stack_symbol)
    D=inputstr

    #print("序号 ",cnt," 栈 ",stack," 符号 ",stack_symbol," 输入 ",inputstr," 动作 ",end='')
    s=stack[-1]#s代表栈顶的状态 初始为0
    tmp=table.cell_value(s+1,col[a])#action[s,a]
    
    #调用错误恢复例程
    if len(tmp)==0:
        E="Error"
        #print("Error")
        tb.add_row([A,B,C,D,E])
        break
    #移入
    elif tmp[0]=="s":
        num=(int)(tmp[1:])#取出数值
        stack.append(num)
        stack_symbol.append(a)
        inputstr=inputstr[1:]#从输入中删除
        a=inputstr[0]#令a为下一个输入符号
        E="移入"
        #print("移入")
    #规约A->β
    elif tmp[0]=="r":
        
        num=(int)(tmp[1:])+1#取出数值
        #print("根据",production[num],"规约")
        beta_len=len(production[num])-2#β长度为产生式长度减去2
        #从符号栈中弹出产生式体的β长度个符号
        while(beta_len):
            stack_symbol.pop()#从符号栈中弹出
            stack.pop()#从状态栈弹出
            beta_len-=1
        t=stack[-1]#令t为当前栈顶状态
        ttt=table.cell_value(t+1,col[production[num][0]])

        stack.append(int(ttt))#GOTO[t,A]状态压入状态栈
        stack_symbol.append(production[num][0])#规约得到的产生式头(A)压入符号栈
        E="根据"+production[num]+"规约"
    #接受
    elif tmp[0]=="a":
        E="接受"
        tb.add_row([A,B,C,D,E])
        #print("接受")
        break
    #未知错误
    else:
        print("Error")
        break
    tb.add_row([A,B,C,D,E])
    cnt+=1
    #print("---------------------------------------------------")

#表格各列对齐方式
tb.align[" "] = "r"
tb.align["栈"] = "l"
tb.align["符号"] = "l"
tb.align["输入"] = "r"
tb.align["动作"] = "l"
#输出表格
print(tb)
