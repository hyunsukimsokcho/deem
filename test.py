from Component.duplicator import Duplicator
from Component.cleaner import Cleaner
from Component.utils import Timer

GermanDuplicator = Duplicator(category="GermanBank")
t = Timer()
print(GermanDuplicator.train_data)
t.tictic()

#GermanDuplicator.parallel_duplicate(5, 4)
#t.toctoc("PARALLEL DUPLICATE")
#print(GermanDuplicator.train_data)
#print(GermanDuplicator.train_data.index.tolist())

GermanCleaner = Cleaner(data=GermanDuplicator.train_data)
t.tictic()
GermanCleaner.literal_clean()
t.toctoc("LITERAL CLEAN")

print(GermanCleaner.data)
