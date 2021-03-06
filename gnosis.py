import random
import logging


logging.basicConfig(level=logging.DEBUG)


def books_from_data(filepath):
    '''
    Convert a txt file containing data about books
    in a usable data structure.
    :param filepath: path to file
    :return: list of dicts
    '''
    data =[]
    with open(filepath) as books:
        for book in books:
            author, name = book.split(',')
            data.append({'Author': author, 'Book': name.strip('\n')})
    return data


def users_from_data(filepath):
    '''
    Convert a txt file containing user names and their ratings for
    certain books into a usable data structure
    :param filepath: path to file
    :return: dict
    '''
    names = []
    ratings = []
    index = 0
    with open(filepath) as users:
        for line in users:
            user = line.split('\n')[0]
            if index % 2 == 0:
                names.append(user)
            else:
                rating = user.split(' ')[:-1]
                rating = [int(el) for el in rating]
                ratings.append(rating)
            index += 1
    return dict(zip(names, ratings))


def similarity(ratings_a, ratings_b):
    '''
    calculates the similarity between two lists of book ratings
    :param ratings_a: list of book ratings
    :param ratings_b: list of book ratings
    :return: int
    '''
    return sum([rating_a * rating_b for rating_a, rating_b in zip(ratings_a, ratings_b)])


def check_user(name):
    '''
    checks if user exists in user data structure. if not the user is prompted to
    rate 20% of the books in the books data structure.
    :param name: name of user
    :return: list
    '''
    if name not in users:
        logging.info('Redo: check user {} not in users'.format(name))
        books_rated = 0
        ratings = []
        for i,_ in enumerate(books):
            ratings.append(0)

        while books_rated < len(books) * 0.2:
            book_random = random.randint(0, len(books) -1)
            book_name = books[book_random]['Book']
            rating = int(input('Enter rating for {} '.format(book_name)))

            check = False
            while not check:
                if rating in [-5, -3, -1, 1, 3, 5]:
                    check = True
                else:
                    print('Error: Invalid Rating!')
                    rating = int(input('Enter rating for {} '.format(book_name)))
            ratings[book_random] = rating
            books_rated += 1
    else:
        ratings = users[name]
    return ratings


def most_similar(name, ratings):
    '''
    calculates a list of similar users based on the similarity of book taste
    :param name: name of user
    :param ratings: list of book ratings
    :return: list of lists
    '''
    scores = []
    for user in users:
        if user != name:
            score = similarity(ratings, users[user])
            scores.append([score, user])

    scores = sorted(scores, reverse=True)
    return scores


def book_recommendations(amount=10):
    '''
    Finds a certain number of books based on the book taste for a specific user
    :param amount: amount of books
    :return: list of dicts
    '''
    books_to_show = []
    user_index = 0
    while len(books_to_show) < amount:
        for i, _ in enumerate(books):
            user_name = similar_users[user_index][1]
            book_name = books[i]['Book']
            if users[user_name][i] >= 3 and user_ratings[i] == 0 and book_name not in books_to_show:
                books_to_show.append({'Name':book_name , 'By': user_name})
        user_index += 1
    return books_to_show[:amount]


# Main Program
books = books_from_data('books.txt')
users = users_from_data('ratings.txt')
username = input('Enter User Name: ')
user_ratings = check_user(username)
similar_users = most_similar(username, user_ratings)
book_amount = int(input('How many books would you like? '))
logging.debug('Checking if book_amount : {} is less than total books : {}'.format(book_amount, len(books)))
check = False
while not check:
    if book_amount <= len(books):
        check = True
    else:
        print('Error: Invalid Amount!')
        book_amount = int(input('How many books would you like? '))

books_list = book_recommendations(book_amount)
print(len(books_list))
# Printing results
print('Book Recommendations for {}'.format(username))
print('----------------------------')
print('Number of books: {}'.format(book_amount))
for book in books_list:
    print('{} recommended by {}'.format(book['Name'], book['By']))

# Writing results to output.txt
#with open('output.txt', 'w') as output:
#    output.write('Book Recommendations for {}\n'.format(username))
#    output.write('----------------------------\n')
#    output.write('Number of books: {}\n'.format(book_amount))
 #   for book in books_list:
  #    output.write('{} recommended by {}\n'.format(book['Name'], book['By']))