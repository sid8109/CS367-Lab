# state - pair of indexes of two docs.
# edit distance function to compare two words. use this to calculate edit distance of all words in the pair of sentences.
# for heuristic: do this brute.
# to calculate it efficiently, start from m,n and do {-1,0} {0,-1} {-1,-1} and do this upto 0,0
# from state = [i,j], for f for: [i+1,j+1]=cost+h[i+1,j+1] [i,j+1]=h[i,j+1]+all words in i [i+1,j]=h[i+1,j]+all words in j

sentences1=[]
with open('input1.txt', 'r') as f:
    for line in f:
        sentences1.append(line.strip())

sentences2=[]
with open('input2.txt', 'r') as f:
    for line in f:
        sentences2.append(line.strip())


words1=[]
letters1=[]
for sentence in sentences1:
    temp = sentence.split(' ')
    words1.append(temp)
    x=0
    for word in temp:
        x+=len(word)
    letters1.append(x)


words2=[]
letters2=[]
for sentence in sentences2:
    temp = sentence.split()
    words2.append(temp)
    x=0
    for word in temp:
        x+=len(word)
    letters2.append(x)

def edit_distance(word1, word2):
    m=len(word1)
    n=len(word2)
    dp=[[0 for i in range(n+1)] for j in range(m+1)]
    for i in range(m+1):
        for j in range(n+1):
            if i == 0:
                dp[i][j]=j
            elif j == 0:
                dp[i][j]=i
            elif word1[i-1] == word2[j-1]:
                dp[i][j]=dp[i-1][j-1]
            else:
                dp[i][j]=1+min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    # print(word1,word2,dp[m][n])
    return dp[m][n]

def heuristic(sent1, sent2):
    words1 = sent1.split(' ')
    words2 = sent2.split(' ')
    n=len(words1)
    m=len(words2)
    # comp=0
    # i=0
    # j=0
    # while(i<n and j<m):
    #     comp+=edit_distance(words1[i],words2[j])
    #     i+=1
    #     j+=1
    # return comp
    dp = [[0 for i in range(n+1)] for j in range(m+1)]
    for i in range(m+1):
        for j in range(n+1):
            if(i==0):
                if(j==0):
                    dp[i][j]=0
                else:
                    dp[i][j]=dp[i][j-1]+len(words1[j-1])
            elif(j==0):
                if(i==0):
                    dp[i][j]=0
                else:    
                    dp[i][j]=dp[i-1][j]+len(words2[i-1])
            else:
                dp[i][j]=min(dp[i-1][j-1] + edit_distance(words2[i-1], words1[j-1]), dp[i-1][j] + len(words2[i-1]), dp[i][j-1] + len(words1[j-1]))
    # # for i in range(m+1):
    # #     for j in range(n+1):
    # #         print(dp[i][j], end=" ")
    # #     print("\n")
    
    return dp[m][n]

heuristic_ = [[0 for i in range(len(sentences1))] for j in range(len(sentences2))]
for i in range(len(sentences1)-1,-1,-1):
    for j in range(len(sentences2)-1,-1,-1):
        if(i==len(sentences1)-1 and j==len(sentences2)-1):
            heuristic_[i][j]=heuristic(sentences1[i],sentences2[j])
            continue
        heuristic_[i][j]= 1e18
        if(i+1<len(sentences1)):
            s=0
            for word in sentences1[i]:
                s+=len(word)
            heuristic_[i][j]=min(heuristic_[i][j],heuristic_[i+1][j]+s)
        if(j+1<len(sentences2)):
            s=0
            for word in sentences2[j]:
                s+=len(word)
            heuristic_[i][j]=min(heuristic_[i][j],heuristic_[i][j+1]+s)
        if(i+1<len(sentences1) and j+1<len(sentences2)):
            heuristic_[i][j]=min(heuristic_[i][j],heuristic_[i+1][j+1])
        heuristic_[i][j]+=heuristic(sentences1[i],sentences2[j])

def search():
    state = [0,0,0]
    # print(state[0])
    # print(state[1])
    # print(state[2])
    # print(len(sentences1))
    # print(len(sentences2))
    while(state[0]<len(sentences1) and state[1]<len(sentences2)):
        # print("here")
        pos = (state[0],state[1])
        cost = state[2]
        # print(pos)
        # print("cost: ",cost)
        moves = []
        if(pos[0]+1<len(sentences1)):
            h = heuristic_[pos[0]+1][pos[1]]+letters1[pos[0]]
            moves.append([pos[0]+1,pos[1],h+cost+letters1[pos[0]]])
        if(pos[1]+1<len(sentences2)):
            h = heuristic_[pos[0]][pos[1]+1]+letters2[pos[1]]
            moves.append([pos[0],pos[1]+1,h+cost+letters2[pos[1]]])
        if(pos[0]+1<len(sentences1) and pos[1]+1<len(sentences2)):
            h = heuristic_[pos[0]+1][pos[1]+1]
            c1=heuristic(sentences1[i],sentences2[j])
            # print(c1)
            moves.append([pos[0]+1,pos[1]+1,h+cost+c1])
            h+=letters1[pos[0]]+letters2[pos[1]]
            moves.append([pos[0]+1,pos[1]+1,h+cost])
        moves.sort(key=lambda x: x[2])
        if(len(moves)==0):
            # print("here")
            state[2]+=heuristic_[state[0]][state[1]]
            break
        moves[0][2]-=heuristic_[moves[0][0]][moves[0][1]]
        state = moves[0]
    # print(state[2])
    return state[2]

non_similar_words = search()
similar_words = max(sum(letters1),sum(letters2)) - non_similar_words;

print(similar_words)

ratio = similar_words/(max(sum(letters1),sum(letters2)))
if ratio >= 0.3:
    print("Plagiarism detected")
else:
    print("No plagiarism detected")

# for i in range(len(sentences1)):
#     for j in range(len(words1[i])):
#         print(words1[i][j], end=" ")

# for i in range(len(sentences2)):
#     for j in range(len(words2[i])):
#         print(words2[i][j], end=" ")
# print("this")
# for i in range(len(sentences1)):
#     for j in range(len(sentences2)):
#         print(heuristic_[i][j], end=" ")
#     print("\n")
