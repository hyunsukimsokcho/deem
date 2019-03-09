from Component.duplicator import Duplicator
from Component.cleaner import Cleaner
from Component.utils import Timer

AdultDuplicator = Duplicator(category="AdultCensus")
t = Timer()
print("After Cross-Validation")
print(AdultDuplicator.train_data.shape[0])
t.tictic()
AdultDuplicator.parallel_duplicate(5, 4)
t.toctoc("PARALLEL DUPLICATE")
#print('a', GermanDuplicator.train_data)
#print(GermanDuplicator.train_data.index.tolist())
print("After Parallel Duplication")
print(AdultDuplicator.train_data.shape[0])

#GermanCleaner = Cleaner(data=GermanDuplicator.train_data.copy())
#GermanCleanerLiteral = Cleaner(data=GermanDuplicator.train_data.copy())
#copiedDF = GermanDuplicator.train_data.copy()
#t.tictic()
#GermanCleanerLiteral.literal_clean(copiedDF)
#t.toctoc("LITERAL CLEAN")
#print("After Literal CLEAN")
#print(copiedDF.shape[0])

#t.tictic()
#GermanCleaner.literal_clean(GermanDuplicator.train_data)
#t.toctoc("LITERAL CLEAN")
AdultCleaner = Cleaner(data=AdultDuplicator.train_data)
t.tictic()
AdultCleaner.parallel_clean(100)
t.toctoc("PARALLEL CLEAN")
print("After Parallel Clean")
print(AdultCleaner.data.shape[0])
print(AdultDuplicator.train_data.shape[0])

