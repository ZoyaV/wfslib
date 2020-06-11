

Wfslib - обработка данных датчика волнового фронта.
==================

Загрузка данных 
------------------
По умолчанию модуль имеет работать с двумя типами данных: numpy, hdf. 
Так же в модуль могут быть переданы изображения любого формата, считаные в массив numpy. 
При загрузке данных формата hdf, следует указать путь по которому 
располагаются данные, передав параметр ``dataset_name``

::

    from wfslib.wfs import WFSData	
	
    wfs = WFSData('file.h5', dataset_name = "data")
	

Визуализация геометрии изображения  
------------------
Модуль автоматически вычисляет геометрию снимка. Визуализировать данные с 
расчитанной геометрией можно следующим образом:


::

    wfs.show_geometry()
	
Передав параметр ``show_type = "offsets"`` в каждой субапертуре
будет отображено смещение относительно референсной ячейки. 
Для изменения референсной ячейки, можно выполнить следующую команду ``wfs.reference = 20``.	
Таким образом, референсной ячейкой станет ячейка с номер 20.
По умолчанию при визуализации, сетка геометрии будет отображаться на все изображение. 
Для отображения только качественных ячеек, можно воспользоваться командой
``wfs.good_only = True``.

Полный код для визуализации данных следующий: 
::

    wfs = WFSData(arr)
    wfs.good_only = True
    wfs.reference = 20

    wfs.show_geometry(show_type = "offsets")
	
.. figure:: https://sun9-44.userapi.com/l6oGl5bsW6tTfW29L98EMDl8Y61xx67Ra9ujVw/OUG-BZ8BFmY.jpg
       :scale: 100 %
       :align: center
       :alt: Альтернативный текст

Изменение параметров геометрии
------------------

Если высчитаные параметры геометрии определены не правильно их можно заменить
с помощью метода ``geometry.set_options``. 

Метод принимает следующие параметры:

* cell_width - изменяет размер ячейки;
* border - изменяет расстояние между ячейками;
* shift - кортеж из двух значений, смещение геометрии по x и по y;
* swap - изменение местами значений border и cell_width;
* rotate - поворот изображения. 

Рассчитаные в автоматическом режиме параметры можно получить так ``wfs.geometry.options``

В коде изменение параметров может выглядеть так: 

::

    wfs = WFSData("points.h5", dataset_name = 'data')
    wfs.good_only = True
    wfs.reference = 20
	
    print(wfs.geometry.options)
    wfs.show_geometry()
	
    wfs.geometry.set_options(shift=(64, -38),swap = True, rotate = 1)
    wfs.show_geometry()

.. figure:: https://sun9-55.userapi.com/To130RzlvYMExvkK0Rrz0_Ta5lSrrPZd1DssJg/iVS6h9Ula30.jpg
       :scale: 100 %
       :align: center
       :alt: Альтернативный текст


.. figure:: https://sun9-23.userapi.com/SdQmWktGVIjzfKVh63XT84tMuHBpr2oYfko2Gg/0JKoMLOdml0.jpg
       :scale: 100 %
       :align: center
       :alt: Альтернативный текст


Обращение к субапертурам
------------------

Объект wfs позволяет обращаться и получать информацию в каждой субапертуре.
Сделать это можно так:

::

	import matplotlib.pyplot as plt
	
	plt.subplot(1,2,1)
	plt.imshow(wfs[0][34])
	plt.subplot(1,2,2)
	plt.imshow(wfs[0][14])
	
.. figure:: https://sun9-4.userapi.com/er4u7B2mBIAcam73L0_MgU8pAR3x2RnrTyk8pA/upOyKQGpA1k.jpg
       :scale: 100 %
       :align: center
       :alt: Альтернативный текст

Таким образом отобразяться данные находящиеся на листе с индексом 0, в субапертуре с индексом 34.

Вычисление смещений
------------------

Вычислить смещения можно для либо сразу для определенного листа, либо для определенных субапертур.
Смещения вычисляются относительно референсной ячейки.

``wfs[0].offsets`` - вычислит смещения для листа 0.
``wfs[0].qoffsets`` - ускоренное вычисления смещений.
``wfs[0].get_offset(23)`` - вычислит смещения для листа для субапертуры 23.

Замена функции определения качественных ячеек
------------------
 По умолчанию в модуле ячейка считается качественной, если ее усредненной 
 значение больше std по всему кадру:

 ::

	def qualitative_sub_std(cell, std, mean_val):
        return np.mean(cell) > std
    
 Рассмотрим также функцию, фильтрующую по среднему значению:
 ::

	def qualitative_sub_mean(cell, std, mean_val):
        return np.mean(cell) > mean_val

И по медиане:
 ::

	def qualitative_sub_median(cell, std, mean_val):
		return np.median(cell) > mean_val
 
Результаты:

-------
 ::


	wfs.qualitative_function = qualitative_sub_std
	wfs.show_geometry()
	
Визуализация:

.. figure:: https://sun9-50.userapi.com/j62HJ08jDoo0HurVUsAvZZhNJ3R_g9SeNxty1A/10SZ3LCzMDI.jpg
       :scale: 100 %
       :align: center
       :alt: Альтернативный текст

------
 ::


	wfs.qualitative_function = qualitative_sub_mean
	wfs.show_geometry()

Визуализация:
	
.. figure:: https://sun9-47.userapi.com/KLvFlq9Dy_nf6OVOciLfmJPlvvnYNWvOjA1dPg/B6o9VbOXKgE.jpg
       :scale: 100 %
       :align: center
       :alt: Альтернативный текст

-------
 ::


	wfs.qualitative_function = qualitative_sub_median
	wfs.show_geometry()
	
Визуализация:

.. figure:: https://sun9-35.userapi.com/Oy2-UbtJyhsU4pNLRukGbn4vqhiPlMWp77WwOw/ab97IQUobHQ.jpg
       :scale: 100 %
       :align: center
       :alt: Альтернативный текст



