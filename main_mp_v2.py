from multiprocessing import Process
import os

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

#
# def apiExec(number):
#    """
#    Функция умножитель на два
#    """
#    result = number * 2
#    proc = os.getpid()
#    print('{0} doubled to {1} by process id: {2}'.format(
#       number, result, proc))
#
#
# def nodeExec(exexEntity, arg):
#    """
#    Функция умножитель на два
#    """
#    os.system(routine)
#    proc = os.getpid()
#    # print('{0} doubled to {1} by process id: {2}'.format(
#    #    number, result, proc))

def execWork(exexEntity):
   """
   Функция умножитель на два
   """
   os.system(exexEntity)
   proc = os.getpid()
   # print('{0} doubled to {1} by process id: {2}'.format(
   #    number, result, proc))


if __name__ == '__main__':

   procs = []

   # for index, number in enumerate(numbers):
   #     proc = Process(target=doubler, args=(number,))
   #     procs.append(proc)
   #     proc.start()



   procApi = Process(target=execWork, args=("python ./pipe.py",))
   procs.append(procApi)
   procApi.start()

   nodeExec = Process(target=execWork, args=("cd devYacht && nodemon app.js",))
   procs.append(nodeExec)
   nodeExec.start()





   for proc in procs:
      proc.join()