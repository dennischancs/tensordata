import os
import io
import time
import json
import requests
import concurrent
import pandas as pd
import tensorflow as tf

__all__ = ['ctrip_hotel', 'douban_movies', 'online_shopping_10_cats', 'sina_weibo', 
           'sina_weibo_emotion4', 'takeaway',
          ]
def ctrip_hotel(root):
    """Ctrip hotel reviews datasets.
    
    datasets url:`https://github.com/SophonPlus/ChineseNlpCorpus/blob/
    master/datasets/ChnSentiCorp_htl_all/ChnSentiCorp_htl_all.csv`
    
    Ctrip's review data set contains 7000+ samples, 
    including more than 5,000 positive reviews 
    and more than 2,000 negative reviews
    
    Data storage directory:
    root = `/user/.../mydata`
    chinese_reviews_ctrip_hotel data: 
    `root/chinese_reviews_ctrip_hotel/chinese_reviews_ctrip_hotel.txt`
    `root/chinese_reviews_ctrip_hotel/chinese_reviews_ctrip_hotel.json`
    Args:
        root: str, Store the absolute path of the data directory.
              example:if you want data path is `/user/.../mydata/chinese_reviews_ctrip_hotel`,
              root should be `/user/.../mydata`.
    Returns:
        Store the absolute path of the data directory, is `root/chinese_reviews_ctrip_hotel`.
    """
    start = time.time()
    assert tf.gfile.IsDirectory(root), '`root` should be directory.'
    task_path = os.path.join(root, 'chinese_reviews_ctrip_hotel')
    if tf.gfile.Exists(task_path):
        tf.gfile.DeleteRecursively(task_path)
    tf.gfile.MakeDirs(task_path)
    url_json = 'https://raw.githubusercontent.com/Hourout/datasets/master/nlp/chinese_reviews_ctrip_hotel/chinese_reviews_ctrip_hotel.json'
    url_txt = 'https://raw.githubusercontent.com/SophonPlus/ChineseNlpCorpus/master/datasets/ChnSentiCorp_htl_all/ChnSentiCorp_htl_all.csv'
    s = requests.get(url_json)
    with open(os.path.join(task_path, 'chinese_reviews_ctrip_hotel.json'), 'w') as outfile:
        json.dump(s.json(), outfile, ensure_ascii=False)
        outfile.write('\n')
    s = requests.get(url_txt).content
    data = pd.read_csv(io.StringIO(s.decode('utf-8')))
    data.to_csv(os.path.join(task_path, 'chinese_reviews_ctrip_hotel.txt'), index=False)
    print('chinese_reviews_ctrip_hotel dataset download completed, run time %d min %.2f sec' %divmod((time.time()-start), 60))
    return task_path

def _request_txt(url):
    s = requests.get(url).content
    t = pd.read_csv(io.StringIO(s.decode('utf-8')))
    return t

def douban_movies(root):
    """Chinese douban movies reviews datasets.
        
    Chinese douban movies reviews datasets Includes 28 movies, 
    over 700,000 users, over 2 million ratings.
    
    Data storage directory:
    root = `/user/.../mydata`
    chinese_reviews_douban_movies data: 
    `root/chinese_reviews_douban_movies/chinese_reviews_douban_movies.json`
    `root/chinese_reviews_douban_movies/ratings.txt`
    Args:
        root: str, Store the absolute path of the data directory.
              example:if you want data path is `/user/.../mydata/chinese_reviews_douban_movies`,
              root should be `/user/.../mydata`.
    Returns:
        Store the absolute path of the data directory, is `root/chinese_reviews_douban_movies`.
    """
    start = time.time()
    assert tf.gfile.IsDirectory(root), '`root` should be directory.'
    task_path = os.path.join(root, 'chinese_reviews_douban_movies')
    if tf.gfile.Exists(task_path):
        tf.gfile.DeleteRecursively(task_path)
    tf.gfile.MakeDirs(task_path)
    url_json = 'https://raw.githubusercontent.com/Hourout/datasets/master/nlp/chinese_reviews_douban_movies/chinese_reviews_douban_movies.json'
    url_movies = 'https://raw.githubusercontent.com/Hourout/datasets/master/nlp/chinese_reviews_douban_movies/movies.txt'
    url_ratings = 'https://raw.githubusercontent.com/Hourout/datasets/master/nlp/chinese_reviews_douban_movies/ratings.txt'
    with open(os.path.join(task_path, 'chinese_reviews_douban_movies.json'), 'w') as outfile:
        json.dump(requests.get(url_json).json(), outfile, ensure_ascii=False)
        outfile.write('\n')
    data = pd.read_csv(io.StringIO(requests.get(url_movies).content.decode('utf-8')))
    data.to_csv(os.path.join(task_path, 'movies.txt'), index=False)
    l = [url_ratings[:-4]+str(i)+url_ratings[-4:] for i in range(13)]
    with concurrent.futures.ProcessPoolExecutor() as excutor:
        data = pd.concat(excutor.map(_request_txt, l))
    data.to_csv(os.path.join(task_path, 'ratings.txt'), index=False)
    print('chinese_reviews_douban_movies dataset download completed, run time %d min %.2f sec' %divmod((time.time()-start), 60))
    return task_path

def online_shopping_10_cats(root):
    """Chinese online shopping reviews datasets.
        
    Chinese online shopping reviews datasets contains 60,000+ samples, 
    about 10 categories (books, tablets, mobile phones, fruits, shampoos, 
    water heaters, Mengniu, clothes, computers, hotels),
    including more than 30,000 positive reviews 
    and more than 30,000 negative reviews
    
    Data storage directory:
    root = `/user/.../mydata`
    chinese_reviews_online_shopping_10_cats data: 
    `root/chinese_reviews_online_shopping_10_cats/chinese_reviews_online_shopping_10_cats.json`
    `root/chinese_reviews_online_shopping_10_cats/chinese_reviews_online_shopping_10_cats.txt`
    Args:
        root: str, Store the absolute path of the data directory.
              example:if you want data path is `/user/.../mydata/chinese_reviews_online_shopping_10_cats`,
              root should be `/user/.../mydata`.
    Returns:
        Store the absolute path of the data directory, is `root/chinese_reviews_online_shopping_10_cats`.
    """
    start = time.time()
    assert tf.gfile.IsDirectory(root), '`root` should be directory.'
    task_path = os.path.join(root, 'chinese_reviews_online_shopping_10_cats')
    if tf.gfile.Exists(task_path):
        tf.gfile.DeleteRecursively(task_path)
    tf.gfile.MakeDirs(task_path)
    url_json = 'https://raw.githubusercontent.com/Hourout/datasets/master/nlp/chinese_reviews_online_shopping_10_cats/chinese_reviews_online_shopping_10_cats.json'
    url_txt = 'https://raw.githubusercontent.com/Hourout/datasets/master/nlp/chinese_reviews_online_shopping_10_cats/chinese_reviews_online_shopping_10_cats.csv'
    s = requests.get(url_json)
    with open(os.path.join(task_path, 'chinese_reviews_online_shopping_10_cats.json'), 'w') as outfile:
        json.dump(s.json(), outfile, ensure_ascii=False)
        outfile.write('\n')
    s = requests.get(url_txt).content
    data = pd.read_csv(io.StringIO(s.decode('utf-8')))
    data.to_csv(os.path.join(task_path, 'chinese_reviews_online_shopping_10_cats.txt'), index=False)
    print('chinese_reviews_online_shopping_10_cats dataset download completed, run time %d min %.2f sec' %divmod((time.time()-start), 60))
    return task_path

def sina_weibo(root):
    """Chinese Sina weibo reviews datasets.
        
    Chinese Sina weibo reviews datasets contains 110,000+ samples, 
    including more than 59,000 positive reviews 
    and more than 59,000 negative reviews
    
    Data storage directory:
    root = `/user/.../mydata`
    chinese_reviews_sina_weibo data: 
    `root/chinese_reviews_sina_weibo/chinese_reviews_sina_weibo.json`
    `root/chinese_reviews_sina_weibo/chinese_reviews_sina_weibo.txt`
    Args:
        root: str, Store the absolute path of the data directory.
              example:if you want data path is `/user/.../mydata/chinese_reviews_sina_weibo`,
              root should be `/user/.../mydata`.
    Returns:
        Store the absolute path of the data directory, is `root/chinese_reviews_sina_weibo`.
    """
    start = time.time()
    assert tf.gfile.IsDirectory(root), '`root` should be directory.'
    task_path = os.path.join(root, 'chinese_reviews_sina_weibo')
    if tf.gfile.Exists(task_path):
        tf.gfile.DeleteRecursively(task_path)
    tf.gfile.MakeDirs(task_path)
    url_json = 'https://raw.githubusercontent.com/Hourout/datasets/master/nlp/chinese_reviews_sina_weibo/chinese_reviews_sina_weibo.json'
    url_txt = 'https://raw.githubusercontent.com/Hourout/datasets/master/nlp/chinese_reviews_sina_weibo/chinese_reviews_sina_weibo.csv'
    s = requests.get(url_json)
    with open(os.path.join(task_path, 'chinese_reviews_sina_weibo.json'), 'w') as outfile:
        json.dump(s.json(), outfile, ensure_ascii=False)
        outfile.write('\n')
    s = requests.get(url_txt).content
    data = pd.read_csv(io.StringIO(s.decode('utf-8')))
    data.to_csv(os.path.join(task_path, 'chinese_reviews_sina_weibo.txt'), index=False)
    print('chinese_reviews_sina_weibo dataset download completed, run time %d min %.2f sec' %divmod((time.time()-start), 60))
    return task_path

def sina_weibo_emotion4(root):
    """Chinese Sina weibo 4 emotion reviews datasets.
        
    Chinese Sina weibo reviews datasets contains 360,000+ samples, 
    contains 4 emotions, including about 200,000 joys, 
    anger, disgust, and low, more than 50,000.
    
    Data storage directory:
    root = `/user/.../mydata`
    chinese_reviews_sina_weibo_emotion4 data: 
    `root/chinese_reviews_sina_weibo_emotion4/chinese_reviews_sina_weibo_emotion4.json`
    `root/chinese_reviews_sina_weibo_emotion4/chinese_reviews_sina_weibo_emotion4.txt`
    Args:
        root: str, Store the absolute path of the data directory.
              example:if you want data path is `/user/.../mydata/chinese_reviews_sina_weibo_emotion4`,
              root should be `/user/.../mydata`.
    Returns:
        Store the absolute path of the data directory, is `root/chinese_reviews_sina_weibo_emotion4`.
    """
    start = time.time()
    assert tf.gfile.IsDirectory(root), '`root` should be directory.'
    task_path = os.path.join(root, 'chinese_reviews_sina_weibo_emotion4')
    if tf.gfile.Exists(task_path):
        tf.gfile.DeleteRecursively(task_path)
    tf.gfile.MakeDirs(task_path)
    url_json = 'https://raw.githubusercontent.com/Hourout/datasets/master/nlp/chinese_reviews_sina_weibo_emotion4/chinese_reviews_sina_weibo_emotion4.json'
    url_txt = ['https://raw.githubusercontent.com/Hourout/datasets/master/nlp/chinese_reviews_sina_weibo_emotion4/chinese_reviews_sina_weibo_emotion4_01.txt',
               'https://raw.githubusercontent.com/Hourout/datasets/master/nlp/chinese_reviews_sina_weibo_emotion4/chinese_reviews_sina_weibo_emotion4_02.txt',
               'https://raw.githubusercontent.com/Hourout/datasets/master/nlp/chinese_reviews_sina_weibo_emotion4/chinese_reviews_sina_weibo_emotion4_03.txt',]
    s = requests.get(url_json)
    with open(os.path.join(task_path, 'chinese_reviews_sina_weibo_emotion4.json'), 'w') as outfile:
        json.dump(s.json(), outfile, ensure_ascii=False)
        outfile.write('\n')
    data = pd.DataFrame()
    for url in url_txt:
        s = requests.get(url).content
        data = pd.concat([data, pd.read_csv(io.StringIO(s.decode('utf-8')))])
    data.to_csv(os.path.join(task_path, 'chinese_reviews_sina_weibo_emotion4.txt'), index=False)
    print('chinese_reviews_sina_weibo_emotion4 dataset download completed, run time %d min %.2f sec' %divmod((time.time()-start), 60))
    return task_path

def takeaway(root):
    """Chinese takeaway reviews datasets.
    
    datasets url:`https://github.com/SophonPlus/ChineseNlpCorpus/blob/master/datasets/waimai_10k/waimai_10k.csv`
    
    Chinese takeaway reviews datasets contains 12,000+ samples, 
    including more than 4,000 positive reviews 
    and more than 8,000 negative reviews
    
    Data storage directory:
    root = `/user/.../mydata`
    chinese_reviews_takeaway data: 
    `root/chinese_reviews_takeaway/chinese_reviews_takeaway.json`
    `root/chinese_reviews_takeaway/chinese_reviews_takeaway.txt`
    Args:
        root: str, Store the absolute path of the data directory.
              example:if you want data path is `/user/.../mydata/chinese_reviews_takeaway`,
              root should be `/user/.../mydata`.
    Returns:
        Store the absolute path of the data directory, is `root/chinese_reviews_takeaway`.
    """
    start = time.time()
    assert tf.gfile.IsDirectory(root), '`root` should be directory.'
    task_path = os.path.join(root, 'chinese_reviews_takeaway')
    if tf.gfile.Exists(task_path):
        tf.gfile.DeleteRecursively(task_path)
    tf.gfile.MakeDirs(task_path)
    url_json = 'https://raw.githubusercontent.com/Hourout/datasets/master/nlp/chinese_reviews_takeaway/chinese_reviews_takeaway.json'
    url_txt = 'https://raw.githubusercontent.com/SophonPlus/ChineseNlpCorpus/master/datasets/waimai_10k/waimai_10k.csv'
    s = requests.get(url_json)
    with open(os.path.join(task_path, 'chinese_reviews_takeaway.json'), 'w') as outfile:
        json.dump(s.json(), outfile, ensure_ascii=False)
        outfile.write('\n')
    s = requests.get(url_txt).content
    data = pd.read_csv(io.StringIO(s.decode('utf-8')))
    data.to_csv(os.path.join(task_path, 'chinese_reviews_takeaway.txt'), index=False)
    print('chinese_reviews_takeaway dataset download completed, run time %d min %.2f sec' %divmod((time.time()-start), 60))
    return task_path
