import discord
import asyncio
import os, io, sys
import logging
import operator
import collections
import random

class SortingHat:
    def __init__(self, client):
        self.__running = False
        self.current_question = None
        self._client = client
        self.gryffindor = 0
        self.hufflepuff = 0
        self.ravenclaw = 0
        self.slytherin = 0

    def started(self):
        #check whether sorting quiz is in progress
        return self.__running
    def question_in_progress(self):
        return self.__current_question is not None

    async def start(self, message):
        sorting_song1 = '*Oh you may not think I\'m pretty,*\n*But don\'t judge on what you see,*\n*I\'ll eat myself if you can find*\n*A smarter hat than me.*\n\n'
        sorting_song2 = '*You can keep your bowlers black,*\n*Your top hats sleek and tall,*\n*For I\'m the Hogwarts Sorting Hat*\n*And I can cap them all.*\n\n'
        sorting_song3 = '*There\'s nothing hidden in your head*\n*The Sorting Hat can\'t see,*\n*So try me on and I will tell you*\n*Where you out to be.*\n\n'
        sorting_song4 = '*You might belong in Gryffindor,*\n*Where dwell the brave at heart,*\n*Their daring, nerve, and chivalry*\n*Set Gryffindors apart;*\n\n'
        sorting_song5 = '*You might belong in Hufflepuff,*\n*Where they are just and loyal,*\n*Those patient Hufflepuffs are true*\n*And unafraid of toil;*\n\n'
        sorting_song6 = '*Or yet in wise old Ravenclaw*\n*If you\'ve a ready mind,*\n*Where those of wit and learning,*\n*Will always find their kind;*\n\n'
        sorting_song7 = '*Or perhaps in Slytherin*\n*You\'ll make your real friends,*\n*Those cunning folks use any means*\n*To achieve their ends.*\n\n'
        sorting_song8 = '*So put me on! Don\'t be afraid!*\n*And don\'t get in a flap!*\n*You\'re in safe hands (though I have none)*\n*For I\'m a thinking cap!*\n\n'

        if self.__running:
            await self._client.send_message(message.channel, ('Someone is aready being sorted, hang on a tick, {}!').format(message.author.display_name))
        else:
            await self.reset()
            self._channel = message.channel
            await self._client.send_message(self._channel, sorting_song1)
            await asyncio.sleep(1)
            await self._client.send_message(self._channel, sorting_song2)
            await asyncio.sleep(1)
            await self._client.send_message(self._channel, sorting_song3)
            await asyncio.sleep(1)
            await self._client.send_message(self._channel, sorting_song4)
            await asyncio.sleep(1)
            await self._client.send_message(self._channel, sorting_song5)
            await asyncio.sleep(1)
            await self._client.send_message(self._channel, sorting_song6)
            await asyncio.sleep(1)
            await self._client.send_message(self._channel, sorting_song7)
            await asyncio.sleep(1)
            await self._client.send_message(self._channel, sorting_song8)

            await asyncio.sleep(2)
            sort = 'Are you ready to be sorted? Type `Yes` to begin or `!stop` to exit at any time.'
            em = discord.Embed(description = sort)
            await self._client.send_message(self._channel, embed = em)
            self.__running = True

    async def reset(self):
        if self.__running:
            await self.stop(self._channel)
        self.current_question = None
        self.__running = False

    async def stop(self, channel):
        if self.__running:
            await self._client.send_message(channel, 'Sorting Ceremony has ended or been interrupted.')
            self.current_question = None
            self.__running = False
        else:
            await self._client.send_message(channel, 'Sorting Ceremony has not begun. To start, type `!sort`')

    async def clear(self, channel, number):
        mgs = []
        number = int(number) # number of messages to clear
        async for x in self._client.logs_from(channel, limit = number):
            mgs.append(x)
        await self._client.delete_messages(mgs)

    async def quiz(self, message):
        if self.__running:

			### QUESTION 1 ###

            footer = 'questions from pottermore.com (1/10)'
            q1 = 'What would you least like to be called?\n'
            c1 = 'A. Ignorant\nB. Cowardly\nC. Selfish\nD. Ordinary'
            em = discord.Embed(title = q1, description = c1)
            em.set_footer(text=footer)
            await self._client.send_message(self._channel, embed=em)

            def check(msg):
                if msg.content.startswith('A') or msg.content.startswith('B') or msg.content.startswith('C') or msg.content.startswith('D'):
                    return True

            answer = await self._client.wait_for_message(author=message.author, check=check)
            answer = answer.content.strip()

            if answer == 'A':
                self.ravenclaw+=1
            elif answer == 'B':
                self.gryffindor+=1
            elif answer == 'C':
                self.hufflepuff+=1
            elif answer == 'D':
                self.slytherin+=1
            await self._client.send_message(message.channel, ('You have answered `{}`').format(answer))
            await asyncio.sleep(1)
            await self.clear(message.channel, 4)

            ### QUESTION 2 ###

            footer = 'questions from pottermore.com (2/10)'
            #await asyncio.sleep(1)
            q1 = 'When you\'re dead, what do you want people to do when they think of you?\n'
            c1 = 'A. Miss me and smile\nB. Think of my achievements\nC. Tell stories about my adventures\nD. I don\'t care what people think of me when I\'m dead; it\'s when I\'m alive that counts'
            em = discord.Embed(title = q1, description = c1)
            em.set_footer(text=footer)
            await self._client.send_message(self._channel, embed=em)

            def check(msg):
                if msg.content.startswith('A') or msg.content.startswith('B') or msg.content.startswith('C') or msg.content.startswith('D'):
                    return True

            answer = await self._client.wait_for_message(author=message.author, check=check)
            answer = answer.content.strip()

            if answer == 'A':
                self.hufflepuff+=1
            elif answer == 'B':
                self.ravenclaw+=1
            elif answer == 'C':
                self.gryffindor+=1
            elif answer == 'D':
                self.slytherin+=1
            await self._client.send_message(message.channel, ('You have answered `{}`').format(answer))
            await asyncio.sleep(1)
            await self.clear(message.channel, 3)

            ### QUESTION 3 ###

            footer = 'questions from pottermore.com (3/10)'
            q1 = 'What kind of instrument most pleases your ear?\n'
            c1 = 'A. Piano\nB. Violin\nC. Trumpet\nD. Drums'
            em = discord.Embed(title = q1, description = c1)
            em.set_footer(text=footer)
            await self._client.send_message(self._channel, embed=em)

            def check(msg):
                if msg.content.startswith('A') or msg.content.startswith('B') or msg.content.startswith('C') or msg.content.startswith('D'):
                    return True

            answer = await self._client.wait_for_message(author=message.author, check=check)
            answer = answer.content.strip()

            if answer == 'A':
                self.ravenclaw+=1
            elif answer == 'B':
                self.slytherin+=1
            elif answer == 'C':
                self.hufflepuff+=1
            elif answer == 'D':
                self.gryffindor+=1
            await self._client.send_message(message.channel, ('You have answered `{}`').format(answer))
            await asyncio.sleep(1)
            await self.clear(message.channel, 3)

            ### QUESTION 4 ###

            footer = 'questions from pottermore.com (4/10)'
            q1 = 'If you were attending Hogwarts, which pet would you choose to take with you?\n'
            c1 = 'A. Barn owl\nB. White cat\nC. Ginger cat\nD. Tawny owl\nE. Dragon toad\nF. Common toad\nG. Snowy owl\nH. Black cat'
            em = discord.Embed(title = q1, description = c1)
            em.set_footer(text=footer)
            await self._client.send_message(self._channel, embed=em)

            def check(msg):
                if msg.content.startswith('A') or msg.content.startswith('B') or msg.content.startswith('C') or msg.content.startswith('D') or msg.content.startswith('E') or msg.content.startswith('F') or msg.content.startswith('G') or msg.content.startswith('H'):
                    return True

            answer = await self._client.wait_for_message(author=message.author, check=check)
            answer = answer.content.strip()

            if answer == 'A':
                self.ravenclaw+=1 #
                self.gryffindor+=0.25
            elif answer == 'B':
                self.slytherin+=1
                self.gryffindor+=0.25
            elif answer == 'C':
                self.slytherin+=1
                self.gryffindor+=0.25
            elif answer == 'D':
                self.ravenclaw+=1
                self.gryffindor+=0.25
            elif answer == 'E':
                self.gryffindor+=0.5
                self.hufflepuff+=0.5
            elif answer == 'F':
                self.hufflepuff+=1
                self.gryffindor+=0.25
            elif answer == 'G':
                self.gryffindor+=0.25
                self.ravenclaw+=0.5
                self.hufflepuff+=0.5
            elif answer == 'H':
                self.slytherin+=1
                self.gryffindor+=0.25
            await self._client.send_message(message.channel, ('You have answered `{}`').format(answer))
            await asyncio.sleep(1)
            await self.clear(message.channel, 3)

            ### QUESTION 5 ###

            footer = 'questions from pottermore.com (5/10)'
            q1 = 'Four boxes are set before you. Which do you open?\n'
            c1 = 'A. A plain jet black box with a silver rune that you know to be the mark of Merlin\nB. A golden box with carved feet that warns secret knowledge and unbearable temptation lurk within\nC. A plain pewter box that says "I open only for the worthy"\nD. A tortoiseshell box that sounds like something living is squeaking inside'
            em = discord.Embed(title = q1, description = c1)
            em.set_footer(text=footer)
            await self._client.send_message(self._channel, embed=em)

            def check(msg):
                if msg.content.startswith('A') or msg.content.startswith('B') or msg.content.startswith('C') or msg.content.startswith('D'):
                    return True

            answer = await self._client.wait_for_message(author=message.author, check=check)
            answer = answer.content.strip()

            if answer == 'A':
                self.slytherin+=1
            elif answer == 'B':
                self.ravenclaw+=1
            elif answer == 'C':
                self.gryffindor+=1
            elif answer == 'D':
                self.hufflepuff+=1
            await self._client.send_message(message.channel, ('You have answered `{}`').format(answer))
            await asyncio.sleep(1)
            await self.clear(message.channel, 3)

            ### QUESTION 6 ###

            footer = 'questions from pottermore.com (6/10)'
            q1 = 'What would you rather be?\n'
            c1 = 'A. Trusted\nB. Liked\nC. Praised\nD. Feared\nE. Envied\nF. Imitated'
            em = discord.Embed(title = q1, description = c1)
            em.set_footer(text=footer)
            await self._client.send_message(self._channel, embed=em)

            def check(msg):
                if msg.content.startswith('A') or msg.content.startswith('B') or msg.content.startswith('C') or msg.content.startswith('D') or msg.content.startswith('E') or msg.content.startswith('F'):
                    return True

            answer = await self._client.wait_for_message(author=message.author, check=check)
            answer = answer.content.strip()

            if answer == 'A':
                self.hufflepuff+=1
                self.gryffindor+=1
            elif answer == 'B':
                self.hufflepuff+=1
            elif answer == 'C':
                self.gryffindor+=1
                self.slytherin+=0.5
            elif answer == 'D':
                self.slytherin+=1
            elif answer == 'E':
                self.ravenclaw+=1
                self.slytherin+=1
            elif answer == 'F':
                self.ravenclaw+=1
            await self._client.send_message(message.channel, ('You have answered `{}`').format(answer))
            await asyncio.sleep(1)
            await self.clear(message.channel, 3)

            ### QUESTION 7 ###

            footer = 'questions from pottermore.com (7/10)'
            q1 = 'Which path do you take?\n'
            c1 = 'A. A twisting leafy path through the woods\nB. A dark, lantern-lit alley\nC. A wide, sunny, grassy path\nD. A cobblestone street lined with ancient buildings'
            em = discord.Embed(title = q1, description = c1)
            em.set_footer(text=footer)
            await self._client.send_message(self._channel, embed=em)

            def check(msg):
                if msg.content.startswith('A') or msg.content.startswith('B') or msg.content.startswith('C') or msg.content.startswith('D'):
                    return True

            answer = await self._client.wait_for_message(author=message.author, check=check)
            answer = answer.content.strip()

            if answer == 'A':
                self.gryffindor+=1
            elif answer == 'B':
                self.slytherin+=1
            elif answer == 'C':
                self.hufflepuff+=1
            elif answer == 'D':
                self.ravenclaw+=1
            await self._client.send_message(message.channel, ('You have answered `{}`').format(answer))
            await asyncio.sleep(1)
            await self.clear(message.channel, 3)

            ### QUESTION 8 ###

            footer = 'questions from pottermore.com (8/10)'
            q1 = 'If you could have one superpower, which would you choose?\n'
            c1 = 'A. Read minds\nB. Invisibility\nC. Change the past\nD. Change your appearance\nE. Talk to animals\nF. Superstrength'
            em = discord.Embed(title = q1, description = c1)
            em.set_footer(text=footer)
            await self._client.send_message(self._channel, embed=em)

            def check(msg):
                if msg.content.startswith('A') or msg.content.startswith('B') or msg.content.startswith('C') or msg.content.startswith('D') or msg.content.startswith('E') or msg.content.startswith('F'):
                    return True

            answer = await self._client.wait_for_message(author=message.author, check=check)
            answer = answer.content.strip()

            if answer == 'A':
                self.slytherin+=1
                self.ravenclaw+=1
            elif answer == 'B':
                self.gryffindor+=1
                self.hufflepuff+=0.5
            elif answer == 'C':
                self.gryffindor+=0.5
                self.slytherin+=1
            elif answer == 'D':
                self.ravenclaw+=1
                self.gryffindor+=0.5
            elif answer == 'E':
                self.hufflepuff+=1
                self.ravenclaw+=1
            elif answer == 'F':
                self.hufflepuff+=1
                self.slytherin+=0.5
            await self._client.send_message(message.channel, ('You have answered `{}`').format(answer))
            await asyncio.sleep(1)
            await self.clear(message.channel, 3)

            ### QUESTION 9 ###

            footer = 'questions from pottermore.com (9/10)'
            q1 = 'You\'re walking down the street late at night and hear a cry that you\'re fairly sure has a magical source. What do you do?\n'
            c1 = 'A. Withdraw into the shadows, reviewing offensive and defensive spells that might be appropriate\nB. Draw your wand and try to discover the source\nC. Proceed with caution, keeping a hand on your still-concealed wand\nD. Draw your wand and stand your ground'
            em = discord.Embed(title = q1, description = c1)
            em.set_footer(text=footer)
            await self._client.send_message(self._channel, embed=em)

            def check(msg):
                if msg.content.startswith('A') or msg.content.startswith('B') or msg.content.startswith('C') or msg.content.startswith('D'):
                    return True

            answer = await self._client.wait_for_message(author=message.author, check=check)
            answer = answer.content.strip()

            if answer == 'A':
                self.ravenclaw+=1
            elif answer == 'B':
                self.gryffindor+=1
            elif answer == 'C':
                self.hufflepuff+=1
            elif answer == 'D':
                self.slytherin+=1
            await self._client.send_message(message.channel, ('You have answered `{}`').format(answer))
            await asyncio.sleep(1)
            await self.clear(message.channel, 3)

            ### QUESTION 10 ###

            footer = 'questions from pottermore.com (10/10)'
            q1 = 'Four goblets are placed before you. Which do you drink?\n'
            c1 = 'A. The golden potion that gives off bright sunspots that dance around the room\nB. The silvery, glittery potion that sparkles as if containing ground diamonds\nC. The thick potion that smells of plums and chocolate\nD. The black, inky potion that gives off fumes that make you see strange visions'
            em = discord.Embed(title = q1, description = c1)
            em.set_footer(text=footer)
            await self._client.send_message(self._channel, embed=em)

            def check(msg):
                if msg.content.startswith('A') or msg.content.startswith('B') or msg.content.startswith('C') or msg.content.startswith('D'):
                    return True

            answer = await self._client.wait_for_message(author=message.author, check=check)
            answer = answer.content.strip()

            if answer == 'A':
                self.gryffindor+=1
            elif answer == 'B':
                self.ravenclaw+=1
            elif answer == 'C':
                self.hufflepuff+=1
            elif answer == 'D':
                self.slytherin+=1
            await self._client.send_message(message.channel, ('You have answered `{}`').format(answer))
            await asyncio.sleep(1)
            await self.clear(message.channel, 3)


            ### WHEN QUESTIONS ARE FINISHED: ###

            houses = {'Gryffindor': self.gryffindor, 'Hufflepuff': self.hufflepuff, 'Ravenclaw': self.ravenclaw, 'Slytherin': self.slytherin}
	     	#houses = collections.defaultdict(houses)
            sorted_h = sorted(houses.items(), key= lambda kv:kv[1], reverse=True)
            sorted_houses = collections.OrderedDict(sorted_h)

            await asyncio.sleep(1)
            if list(sorted_houses.values())[0] == list(sorted_houses.values())[1]:
                house = random.choice([0,1])
                house = list(sorted_houses.keys())[house]
                await self._client.send_message(message.channel, 'Hmm...')
                await asyncio.sleep(2)
                await self._client.send_message(message.channel, 'Difficult...very difficult...')
                await asyncio.sleep(2)
                await self._client.send_message(message.channel, ('Well then... it\'d better be...{}!').format(house))
                await asyncio.sleep(5)
                await self.reset()
                await self.clear(message.channel, 14)
            else:
                house = list(sorted_houses.keys())[0]
                await self._client.send_message(message.channel, ('It\'d better be...{}!').format(house))
                await asyncio.sleep(10)
                await self.reset()
                await self.clear(message.channel, 12)

