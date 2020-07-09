import xlrd#导入用于读取Excel的库
import xlwt#导入用于写入Excel的库
import prettytable as pt#导入用于输出的库
import os
#-------------------------------------------------------------
#从文件中读取产生式
production = []*50 #初始化产生式列表

production_filename = "productions.txt" 
#包含文法产生式的txt文件
"""
文件中产生式的格式为E->E+T则line76表达式末尾为-3
文件中产生式的格式为E#E+T则line76表达式末尾为-2
"""
file = open(production_filename)

while True:
    line = file.readline()#按行读入产生式,每行一个
    if not line:
        break
    line = line.strip("\n")#去除行末换行符
    left = line.split('#')[0]
    if len(line.split('#')[1]) == 0:
        right = []
    else:
        right = line.split('#')[1].split(' ')
    rule = [left, right]
    production.append(rule)#加入产生式列表

file.close()

filename="lr3.xlsx"#语法分析表文件名
data = xlrd.open_workbook(filename)#打开工作簿
table = data.sheets()[0]#打开表格

#table.cell_value(rowx,colx)#返回单元格中的数据

col={}#记录表头 例如:col["a"]=0
for i in range(0,43):#表格lr宽度43
    col[str(table.cell_value(0,i).strip(' '))] = i


#对于输出创建一个workbook 设置编码
workbook = xlwt.Workbook(encoding = 'utf-8')
#创建一个worksheet
worksheet = workbook.add_sheet('Output')
Acol=worksheet.col(0)#xlwt中是行和列都是从0开始计算的
Bcol=worksheet.col(1)
Ccol=worksheet.col(2)
Dcol=worksheet.col(3)
Ecol=worksheet.col(4)


Acol.width=256*5
Bcol.width=256*30
Ccol.width=256*50
Dcol.width=256*50
Ecol.width=256*50


#打开输入的文件
input_filename = "input.txt" 
file = open(input_filename)

line = file.readline()#读入输入内容
line = line.strip("\n")#去除行末换行符
inputstrs=line

file.close()
#inputstrs="if <ident> > <number> then call <ident> $"#输入内容
#inputstrs="if <ident> > <ident> then <ident> : = <ident> + <number> $"
#inputstrs="<ident> : = <number> + const $"
inputstr = inputstrs.split(' ')

a=inputstr[0]#输入内容的第一个符号

stack=[]#状态堆栈
stack.append(0)#压入栈底的0状态

stack_symbol=[]#符号堆栈

cnt=1

tb = pt.PrettyTable()

tb.field_names = [" ","栈", "符号", "输入", "动作"]
#下面循环中用A,B,C,D,E表示这五列
worksheet.write(0,0, label = " ")
worksheet.write(0,1, label = "栈")
worksheet.write(0,2, label = "符号")
worksheet.write(0,3, label = "输入")
worksheet.write(0,4, label = "动作")

#表格各列对齐方式
tb.align[" "] = "r"
tb.align["栈"] = "l"
tb.align["符号"] = "l"
tb.align["输入"] = "r"
tb.align["动作"] = "l"

while True:
    A="("+str(cnt)+")"
    stack_new=[str(x) for x in stack]
    B=" ".join(stack_new)
    C="".join(stack_symbol)
    D=" ".join(inputstr)

    #print("序号 ",cnt," 栈 ",stack," 符号 ",stack_symbol," 输入 ",inputstr," 动作 ",end='')
    s=stack[-1]#s代表栈顶的状态 初始为0
    tmp=str(table.cell_value(s+1,col[a]))#action[s,a]

    #调用错误恢复例程
    if len(tmp)==0:
        E="Error"
        tb.add_row([A,B,C,D,E])
        worksheet.write(cnt,0, label = A)
        worksheet.write(cnt,1, label = B)
        worksheet.write(cnt,2, label = C)
        worksheet.write(cnt,3, label = D)
        worksheet.write(cnt,4, label = E)
        break
    #移入
    elif tmp[0]=="s":
        num=(int)(tmp[1:])#取出数值
        stack.append(num)
        stack_symbol.append(a)
        inputstr=inputstr[1:]#从输入中删除
        a=inputstr[0]#令a为下一个输入符号
        E="移入"
    #规约A->β
    elif tmp[0]=="r":
        num=(int)(tmp[1:])#取出数值
        beta_len = len(production[num][1])#β长度
        #从符号栈中弹出产生式体的β长度个符号
        while(beta_len):
            stack_symbol.pop()#从符号栈中弹出
            stack.pop()#从状态栈弹出
            beta_len-=1
        t=stack[-1]#令t为当前栈顶状态
        ttt=table.cell_value(t+1,col[production[num][0]])

        stack.append(int(ttt))#GOTO[t,A]状态压入状态栈
        stack_symbol.append(production[num][0])#规约得到的产生式头(A)压入符号栈
        E="根据"+production[num][0] + "->"#修改下输出
        for i in range(len(production[num][1])):
            E += production[num][1][i]
        E += "规约"
    #接受
    elif tmp[0]=="a":
        E="接受"
        tb.add_row([A,B,C,D,E])
        worksheet.write(cnt,0, label = A)
        worksheet.write(cnt,1, label = B)
        worksheet.write(cnt,2, label = C)
        worksheet.write(cnt,3, label = D)
        worksheet.write(cnt,4, label = E)
        #print("接受")
        break
    #未知错误
    else:
        print(tmp[0])
        print("Error!!!")
        break
    tb.add_row([A,B,C,D,E])
    worksheet.write(cnt,0, label = A)
    worksheet.write(cnt,1, label = B)
    worksheet.write(cnt,2, label = C)
    worksheet.write(cnt,3, label = D)
    worksheet.write(cnt,4, label = E)

    cnt+=1
    #print("---------------------------------------------------")

#输出表格
print(tb)
#输出表格到文件
workbook.save('output.xls')