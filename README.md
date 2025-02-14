# Gameplan

1. I have all of the data to build a generative AI solution which is able to perform EWT on a dime for any ticker in the U.S. I need to understand how to formulate the problem for the model to be trained. I believe a sequential analysis is necessary. I can use Yahoo Finance to retrieve stock ticker data over various time fidelities. I can then utilize the charts within EWT to label the data with it's respective wave. However, what's the way in which I approach the various degrees? I can approach from the highest level with a model that's trained on 1D setups. It'll be interesting to see the way the model handles incomplete structures, since all structures will be open. However, we can have the model label the sub waves in each structure. We can then operate at various fidelities to abstract deeper information. However, is there a way for us extract the dates of the peak of each wave from the photos scraped? What's the best way to do this one? Is it to take all of a given timeframe and then have the model piece together the time period in which to operate?

1. I need to aggregate the photos. 
2. I need to create a computer vision model to extract the wave label and date from the photo. 
3. I need to do this for SOOOO man stocks to perfect the model. 

1. I aggregate the data with the experts opinion on the wave structure.
2. The model learns the way the experts have labeled the wave structure.
3. I can then provide the model with any wave structure and it will either accurately forecast becasue it's seen it's data before or it will be able to infer based upon previous knowledge.



