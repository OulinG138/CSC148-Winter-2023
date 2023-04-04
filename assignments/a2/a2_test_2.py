import unittest
import os
from tm_trees import *


def repr_tree(tree:TMTree):
    parent_name = "None" if tree._parent_tree is None else tree._parent_tree._name
    if is_leaf(tree):
        return [(tree._name, tree.data_size, parent_name)]
    else:
        temp = []
        for sub in tree._subtrees:
            temp.extend(repr_tree(sub))
        temp += [(tree._name, tree.data_size, parent_name)]
        return temp


def is_leaf(tree):
    return tree._subtrees == []


def set_expanded(tree):
    if is_leaf(tree):
        return [tree._expanded == False]
    else:
        temp = []
        temp.append(tree._expanded)
        for sub in tree._subtrees:
            temp.extend(set_expanded(sub))
        return temp

def set_collapse(tree):
    if is_leaf(tree):
        return [tree._expanded == False]
    else:
        temp = []
        temp.append(not tree._expanded)
        for sub in tree._subtrees:
            temp.extend(set_collapse(sub))
        return temp


def set_size(tree, size):
    if is_leaf(tree):
        tree.data_size = size
    else:
        for sub in tree._subtrees:
            set_size(sub, size)
        tree.data_size = sum([sub.data_size for sub in tree._subtrees])

class a2_test_part1_and_part2(unittest.TestCase):
    def setUp(self):
        self.path = os.path.join('example-directory', "workshop")
        rslt = path_to_nested_tuple(self.path)
        self.FileTree = dir_tree_from_nested_tuple(rslt)

    def test_init(self):
        act = repr_tree(self.FileTree)
        act.sort(key=lambda x:x[1])
        exp = [('Plan.tex', 3, 'activities'), ('reading.md', 7, 'prep'), ('Cats.pdf', 17, 'images'), ('images', 18, 'prep'), ('Q2.pdf', 21, 'images'), ('prep', 26, 'workshop'), ('Q3.pdf', 50, 'images'), ('draft.pptx', 59, 'workshop'), ('images', 72, 'activities'), ('activities', 76, 'workshop'), ('workshop', 162, 'None')]
        self.assertListEqual(act, exp, act)

    def test_tmtree_setup_no_subtree(self):
        t = TMTree('Easy4.0', [], 50)
        self.assertIsInstance(t.data_size, int,
                              'data_size is not instantiated correctly')
        self.assertIsInstance(t._colour, tuple,
                              '_colour is not instantiated correctly')
        self.assertEqual(t.data_size, 50, 'leaf data size is wrong')

    def test_tmtree_setup_with_subtrees(self):
        subtree1 = TMTree('subtree1', [], 10)
        subtree2 = TMTree('subtree2', [], 20)
        t = TMTree('Easy4.0', [subtree1, subtree2], 100)
        self.assertEqual(t.data_size, 130, 'non-leaf data size is wrong')
        self.assertEqual(subtree1._parent_tree, t, 'parent should be set')
        self.assertEqual(subtree2._parent_tree, t, 'parent should be set')

    def test_tmtree_setup_recursive_data_size(self):
        subtree1 = TMTree('subtree1', [TMTree('subtree11', [], 1000)], 10)
        subtree2 = TMTree('subtree2', [TMTree('subtree21', [], 2000)], 20)
        t = TMTree('Easy4.0', [subtree1, subtree2], 666)
        self.assertEqual(t.data_size, 3696, 'non-leaf data size is wrong')



class a2_test_task2(unittest.TestCase):
    def setUp(self):
        self.path = os.path.join('example-directory', "workshop")
        rslt = path_to_nested_tuple(self.path)
        self.FileTree = dir_tree_from_nested_tuple(rslt)

    def test_single_leaf(self):
        leaf = TMTree("leaf", [], 30)
        rect = (0, 0, 100, 100)
        leaf.update_rectangles(rect)
        self.assertCountEqual(leaf.rect, rect, "The leaf should have the exact rect as given")

    def test_one_level_tree(self):
        leaf = TMTree("leaf", [], 30)
        root = TMTree("root", [leaf], 40)
        rect = (0,0,100,100)
        root.update_rectangles(rect)
        self.assertCountEqual(leaf.rect, rect, "")
        self.assertCountEqual(root.rect, rect,  "Since the tree only contains a leaf so the root's rect should be same with leaf")

    def test_two_leaves(self):
        leaf = TMTree("leaf", [], 30)
        leaf2 = TMTree("leaf", [], 70)
        root = TMTree("root", [leaf, leaf2], 0)
        rect = (0, 0, 1000, 100)
        set_expanded(root)
        root.update_rectangles(rect)
        self.assertCountEqual(leaf.rect, (0,0,300,100), "You should calculate the correct proportion of the leaf")
        self.assertCountEqual(leaf2.rect, (300,0,700,100), "You should calculate the correct proportion of the leaf")
        self.assertCountEqual(root.rect, rect, "The root's rect should be exact same with the given argument")

    def test_two_leaves_round(self):
        leaf = TMTree("leaf", [], 30)
        leaf2 = TMTree("leaf", [], 69)
        root = TMTree("root", [leaf, leaf2], 0)
        rect = (0, 0, 200, 100)
        root.update_rectangles(rect)
        self.assertCountEqual(leaf.rect, (0, 0, 60, 100),
                              "Round down the proportion of the leaf")
        self.assertCountEqual(leaf2.rect, (60, 0, 140, 100),
                              "Round down the proportion of the leaf")
        self.assertCountEqual(root.rect, rect,
                              "The root's rect should be exact same with the given argument")

    def test_two_leaves_round2(self):
        leaf = TMTree("leaf", [], 29)
        leaf2 = TMTree("leaf", [], 70)
        root = TMTree("root", [leaf, leaf2], 0)
        rect = (0, 0, 100, 200)
        root.update_rectangles(rect)
        self.assertCountEqual(leaf.rect, (0, 0, 100, 58),
                              "You should calculate the correct proportion of the leaf")
        self.assertCountEqual(leaf2.rect, (0, 58, 100, 142),
                              "You should calculate the correct proportion of the leaf")
        self.assertCountEqual(root.rect, rect,
                              "The root's rect should be exact same with the given argument")

    def test_different_direction(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 30)
        leaf3 = TMTree("leaf3", [], 70)
        internal = TMTree("internal", [leaf2, leaf3], 0)
        root = TMTree("root", [internal, leaf], 0)
        rect = (0, 0, 210, 160)
        set_expanded(root)
        root.update_rectangles(rect)
        self.assertEqual(root.rect, rect, "Root's size should be same with the given argument")
        self.assertEqual(internal.rect, (0,0,140,160), "internal's width takes the 2/3 of the given argument")
        self.assertEqual(leaf.rect, (140, 0, 70, 160), "leaf's width should take 1/3 of the given argument")
        self.assertEqual(leaf2.rect, (0,0, 140, 48), "leaf 2 (The first leaf of internal)'s height should take 3/10 of INTERNAL'S HEIGHT")
        self.assertEqual(leaf3.rect, (0,48, 140, 112), "leaf3 (The second leaf of internal)'s height should take 7/10 of INTERNAL'S HEIGHT")

    def test_two_qual_height_tree(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 50)
        leaf3 = TMTree("leaf3", [], 50)
        leaf4 = TMTree("leaf4", [], 50)
        internal1 = TMTree("internal1", [leaf, leaf2], 0)
        internal2 = TMTree("internal2", [leaf3, leaf4], 0)
        root = TMTree("root", [internal1, internal2], 0)
        rect = (0,0,100,100)
        set_expanded(root)
        root.update_rectangles(rect)
        self.assertEqual(root.rect, rect, "Root's size should be same with the given argument")
        self.assertEqual(internal1.rect, (0, 0, 100, 50), "internal1's height should take half of the root")
        self.assertEqual(internal2.rect, (0, 50, 100, 50), "internal2's height should take half of the root")
        self.assertEqual(leaf.rect, (0, 0, 50, 50), "leaf(the first leaf of internal1)'s weight should take half of the internal1")
        self.assertEqual(leaf2.rect, (50, 0, 50, 50), "leaf2(the second leaf of internal1)'s weight should take second half of the internal1")
        self.assertEqual(leaf3.rect, (0, 50, 50, 50), "leaf3(the first leaf of internal2)'s weight shoudl take half of the internal2's weight")
        self.assertEqual(leaf4.rect, (50, 50, 50, 50), "leaf4(the second leaf of internal2)'s weight should take half of the internal2's weight")

    def test_complicate(self):
        leafI = TMTree("leaf", [], 20)
        leafJ = TMTree("leaf2", [], 15)
        folderD = TMTree("folderD", [leafI, leafJ], 50)
        leafE = TMTree("leaf3", [], 35)
        folderA = TMTree("folderA", [folderD, leafE], 0)
        leafK= TMTree("leafK", [], 40)
        leafL = TMTree("leafL", [], 10)
        folderF = TMTree("folderF", [leafK, leafL], 0)
        leafG = TMTree("leafG", [], 10)
        folderB = TMTree("folderB", [folderF, leafG], 0)
        leafO = TMTree("leafO", [], 20)
        leafP = TMTree("leafP", [], 20)
        folderM = TMTree("leafM", [leafO, leafP], 40)
        leafN =TMTree("leafN", [], 40)
        folderH = TMTree("folderH", [folderM, leafN], 0)
        folderC = TMTree("folderC", [folderH], 0)
        root = TMTree("root", [folderA, folderB, folderC], 0)
        set_expanded(root)
        rect = (0, 0, 210, 60)
        root.update_rectangles(rect)
        self.assertEqual(root.rect, rect)
        self.assertEqual(folderA.rect, (0, 0, 84, 60))
        self.assertEqual(folderB.rect, (84, 0, 42, 60))
        self.assertEqual(folderC.rect, (126, 0, 84, 60))
        self.assertEqual(folderD.rect, (0, 0, 59, 60))
        self.assertEqual(leafE.rect, (59, 0, 25, 60))
        self.assertEqual(leafI.rect, (0, 0, 59, 34))
        self.assertEqual(leafJ.rect, (0, 34, 59, 26))
        self.assertEqual(folderF.rect, (84, 0, 42, 50))
        self.assertEqual(leafG.rect, (84, 50, 42, 10))
        self.assertEqual(leafK.rect, (84, 0, 42, 40))
        self.assertEqual(leafL.rect, (84, 40, 42, 10))
        self.assertEqual(folderH.rect, (126, 0, 84, 60))
        self.assertEqual(folderM.rect, (126, 0, 56, 60))
        self.assertEqual(leafN.rect, (182, 0, 28, 60))
        self.assertEqual(leafO.rect, (126, 0, 56, 30))
        self.assertEqual(leafP.rect, (126, 30, 56, 30))

    def test_get_rectangle_task2(self):
        leaf = TMTree("leaf", [], 30)
        root = TMTree("root", [leaf], 40)
        rect = (0, 0, 100, 100)
        root.update_rectangles(rect)
        set_expanded(root)
        act = root.get_rectangles()
        assert len(act) == 1
        self.assertEqual(act[0][0], rect, "For task 2 you should return every leaf of the DATA tree")

    def test_get_rectangle_task5(self):
        leaf = TMTree("leaf", [], 30)
        root = TMTree("root", [leaf], 40)
        rect = (0, 0, 100, 100)
        root.update_rectangles(rect)
        act = root.get_rectangles()
        assert len(act) == 1
        self.assertEqual(act[0][0], rect, "For task 5 you should return every leaf of the DISPLAYED tree")

    def test_two_leaves_task2(self):
        leaf = TMTree("leaf", [], 30)
        leaf2 = TMTree("leaf", [], 70)
        root = TMTree("root", [leaf, leaf2], 0)
        rect = (0, 0, 1000, 100)
        set_expanded(root)
        root.update_rectangles(rect)
        temp = root.get_rectangles()
        assert len(temp) == 2
        exp = [(0,0,300,100), (300,0,700,100)]
        act = [sub[0] for sub in temp]
        self.assertCountEqual(act, exp, "For task 2 you should return every leaf of the data tree")

    def test_two_leaves_task5(self):
        leaf = TMTree("leaf", [], 30)
        leaf2 = TMTree("leaf", [], 70)
        root = TMTree("root", [leaf, leaf2], 0)
        rect = (0, 0, 1000, 100)
        root.update_rectangles(rect)
        temp = root.get_rectangles()
        assert len(temp) == 2
        exp = [(0, 0, 300, 100), (300, 0, 700, 100)]
        act = [sub[0] for sub in temp]
        self.assertCountEqual(act, exp, "For task 5 you should return every leaf of the displayed tree")

    def test_different_direction_task2(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 30)
        leaf3 = TMTree("leaf3", [], 70)
        internal = TMTree("internal", [leaf2, leaf3], 0)
        root = TMTree("root", [internal, leaf], 0)
        rect = (0, 0, 210, 160)
        exp = [(0, 0, 140, 48), (0, 48, 140, 112), (140, 0, 70, 160)]
        set_expanded(root)
        root.update_rectangles(rect)
        temp = root.get_rectangles()
        assert len(temp) == 3
        act = [sub[0] for sub in temp]
        self.assertCountEqual(act, exp, "For task2 you should return every leaf of the data tree")

    def test_different_direction_task5(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 30)
        leaf3 = TMTree("leaf3", [], 70)
        internal = TMTree("internal", [leaf2, leaf3], 0)
        root = TMTree("root", [internal, leaf], 0)
        rect = (0, 0, 210, 160)
        exp = [(0, 0, 140, 48), (0, 48, 140, 112), (140, 0, 70, 160)]
        root._expanded = True
        root.update_rectangles(rect)
        temp = root.get_rectangles()
        assert len(temp) == 3
        act = [sub[0] for sub in temp]
        self.assertCountEqual(act, exp, "For task5 you should return every leaf of the displayed tree")

    def test_two_qual_height_tree_task2(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 50)
        leaf3 = TMTree("leaf3", [], 50)
        leaf4 = TMTree("leaf4", [], 50)
        internal1 = TMTree("internal1", [leaf, leaf2], 0)
        internal2 = TMTree("internal2", [leaf3, leaf4], 0)
        root = TMTree("root", [internal1, internal2], 0)
        rect = (0,0,100,100)
        set_expanded(root)
        root.update_rectangles(rect)
        exp = [(0, 0, 50, 50), (50, 0, 50, 50), (0, 50, 50, 50), (50, 50, 50, 50)]
        temp = root.get_rectangles()
        assert len(temp) == 4
        act = [sub[0] for sub in temp]
        self.assertCountEqual(act, exp, "For task 2 you should return every leaf in the DATA tree")

    def test_two_qual_height_tree_task5(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 50)
        leaf3 = TMTree("leaf3", [], 50)
        leaf4 = TMTree("leaf4", [], 50)
        internal1 = TMTree("internal1", [leaf, leaf2], 0)
        internal2 = TMTree("internal2", [leaf3, leaf4], 0)
        root = TMTree("root", [internal1, internal2], 0)
        rect = (0,0,100,100)
        root._expanded = True
        root.update_rectangles(rect)
        exp = [(0, 0, 50, 50), (50, 0, 50, 50), (0, 50, 50, 50), (50, 50, 50, 50)]
        temp = root.get_rectangles()
        assert len(temp) == 4
        act = [sub[0] for sub in temp]
        self.assertCountEqual(act, exp, "For task 5 you should only return leaf in the DISPLAY tree")

    def test_two_qual_height_tree_task5_2(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 50)
        leaf3 = TMTree("leaf3", [], 50)
        leaf4 = TMTree("leaf4", [], 50)
        internal1 = TMTree("internal1", [leaf, leaf2], 0)
        internal2 = TMTree("internal2", [leaf3, leaf4], 0)
        root = TMTree("root", [internal1, internal2], 0)
        rect = (0,0,100,100)
        root._expanded = True
        internal2._expanded = True
        root.update_rectangles(rect)
        exp = [(0, 0, 50, 50), (50, 0, 50, 50), (0, 50, 50, 50), (50, 50, 50, 50)]
        temp = root.get_rectangles()
        assert len(temp) == 4
        act = [sub[0] for sub in temp]
        self.assertCountEqual(act, exp, "For task 5 you should only return leaf in the DISPLAY tree")

    def test_complicate_task2(self):
        leafI = TMTree("leaf", [], 20)
        leafJ = TMTree("leaf2", [], 15)
        folderD = TMTree("folderD", [leafI, leafJ], 50)
        leafE = TMTree("leaf3", [], 35)
        folderA = TMTree("folderA", [folderD, leafE], 0)
        leafK= TMTree("leafK", [], 40)
        leafL = TMTree("leafL", [], 10)
        folderF = TMTree("folderF", [leafK, leafL], 0)
        leafG = TMTree("leafG", [], 10)
        folderB = TMTree("folderB", [folderF, leafG], 0)
        leafO = TMTree("leafO", [], 20)
        leafP = TMTree("leafP", [], 20)
        folderM = TMTree("leafM", [leafO, leafP], 40)
        leafN =TMTree("leafN", [], 40)
        folderH = TMTree("folderH", [folderM, leafN], 0)
        folderC = TMTree("folderC", [folderH], 0)
        root = TMTree("root", [folderA, folderB, folderC], 0)
        set_expanded(root)
        rect = (0, 0, 210, 60)
        set_expanded(root)
        root.update_rectangles(rect)
        exp = [(0, 0, 59, 34), (0, 34, 59, 26), (59, 0, 25, 60), (84, 0, 42, 40), (84, 40, 42, 10), (84, 50, 42, 10), (126, 0, 56, 30), (126, 30, 56, 30), (182, 0, 28, 60)]
        temp = root.get_rectangles()
        assert len(temp) == 9
        act = [sub[0] for sub in temp]
        self.assertCountEqual(act, exp,
                              "For task 2 you should return every leaf in the DATA tree")

    def test_complicate_task5(self):
        leafI = TMTree("leaf", [], 20)
        leafJ = TMTree("leaf2", [], 15)
        folderD = TMTree("folderD", [leafI, leafJ], 50)
        leafE = TMTree("leaf3", [], 35)
        folderA = TMTree("folderA", [folderD, leafE], 0)
        leafK = TMTree("leafK", [], 40)
        leafL = TMTree("leafL", [], 10)
        folderF = TMTree("folderF", [leafK, leafL], 0)
        leafG = TMTree("leafG", [], 10)
        folderB = TMTree("folderB", [folderF, leafG], 0)
        leafO = TMTree("leafO", [], 20)
        leafP = TMTree("leafP", [], 20)
        folderM = TMTree("leafM", [leafO, leafP], 40)
        leafN = TMTree("leafN", [], 40)
        folderH = TMTree("folderH", [folderM, leafN], 0)
        folderC = TMTree("folderC", [folderH], 0)
        root = TMTree("root", [folderA, folderB, folderC], 0)
        root._expanded = True
        rect = (0, 0, 210, 60)
        root.update_rectangles(rect)
        exp = [(0, 0, 59, 34), (0, 34, 59, 26), (59, 0, 25, 60), (84, 0, 42, 40), (84, 40, 42, 10), (84, 50, 42, 10), (126, 0, 56, 30), (126, 30, 56, 30), (182, 0, 28, 60)]
        temp = root.get_rectangles()
        assert len(temp) == 9
        act = [sub[0] for sub in temp]
        self.assertCountEqual(act, exp,
                              "For task 5 you should return every leaf in the DISPLAYED tree")

    def test_complicate_task5_2(self):
        leafI = TMTree("leaf", [], 20)
        leafJ = TMTree("leaf2", [], 15)
        folderD = TMTree("folderD", [leafI, leafJ], 50)
        leafE = TMTree("leaf3", [], 35)
        folderA = TMTree("folderA", [folderD, leafE], 0)
        leafK = TMTree("leafK", [], 40)
        leafL = TMTree("leafL", [], 10)
        folderF = TMTree("folderF", [leafK, leafL], 0)
        leafG = TMTree("leafG", [], 10)
        folderB = TMTree("folderB", [folderF, leafG], 0)
        leafO = TMTree("leafO", [], 20)
        leafP = TMTree("leafP", [], 20)
        folderM = TMTree("leafM", [leafO, leafP], 40)
        leafN = TMTree("leafN", [], 40)
        folderH = TMTree("folderH", [folderM, leafN], 0)
        folderC = TMTree("folderC", [folderH], 0)
        root = TMTree("root", [folderA, folderB, folderC], 0)
        root._expanded = True
        folderC._expanded = True
        rect = (0, 0, 210, 60)
        root.update_rectangles(rect)
        exp = [(0, 0, 59, 34), (0, 34, 59, 26), (59, 0, 25, 60), (84, 0, 42, 40), (84, 40, 42, 10), (84, 50, 42, 10), (126, 0, 56, 30), (126, 30, 56, 30), (182, 0, 28, 60)]
        temp = root.get_rectangles()
        assert len(temp) == 9
        act = [sub[0] for sub in temp]
        self.assertCountEqual(act, exp,
                              "For task 5 you should return every leaf in the DISPLAYED tree")

    def test_complicate_task5_3(self):
        leafI = TMTree("leaf", [], 20)
        leafJ = TMTree("leaf2", [], 15)
        folderD = TMTree("folderD", [leafI, leafJ], 50)
        leafE = TMTree("leaf3", [], 35)
        folderA = TMTree("folderA", [folderD, leafE], 0)
        leafK = TMTree("leafK", [], 40)
        leafL = TMTree("leafL", [], 10)
        folderF = TMTree("folderF", [leafK, leafL], 0)
        leafG = TMTree("leafG", [], 10)
        folderB = TMTree("folderB", [folderF, leafG], 0)
        leafO = TMTree("leafO", [], 20)
        leafP = TMTree("leafP", [], 20)
        folderM = TMTree("leafM", [leafO, leafP], 40)
        leafN = TMTree("leafN", [], 40)
        folderH = TMTree("folderH", [folderM, leafN], 0)
        folderC = TMTree("folderC", [folderH], 0)
        root = TMTree("root", [folderA, folderB, folderC], 0)
        root._expanded = True
        folderA._expanded = True
        folderB._expanded = True
        folderC._expanded = True
        rect = (0, 0, 210, 60)
        root.update_rectangles(rect)
        exp = [(0, 0, 59, 34), (0, 34, 59, 26), (59, 0, 25, 60), (84, 0, 42, 40), (84, 40, 42, 10), (84, 50, 42, 10), (126, 0, 56, 30), (126, 30, 56, 30), (182, 0, 28, 60)]
        temp = root.get_rectangles()
        assert len(temp) == 9
        act = [sub[0] for sub in temp]
        self.assertCountEqual(act, exp,
                              "For task 5 you should return every leaf in the DISPLAYED tree")

def eq_tree(tree1, tree2):
    return tree1._name == tree2._name


class a2_test_task3(unittest.TestCase):
    def test_single_leaf(self):
        leaf = TMTree("leaf", [], 50)
        leaf.update_rectangles((0,0,10,20))
        self.assertEqual(leaf.get_tree_at_position((20,30)), None, "This is out of boundary None")

    def test_out_of_boundary(self):
        leaf = TMTree("leaf", [], 50)
        leaf.update_rectangles((0, 0, 10, 20))
        self.assertEqual(leaf.get_tree_at_position((10, 30)), None,
                         "This is out of boundary None")

    def test_out_of_boundary2(self):
        leaf = TMTree("leaf", [], 50)
        leaf.update_rectangles((0, 0, 10, 20))
        self.assertEqual(leaf.get_tree_at_position((0, 30)), None,
                         "This is out of boundary None")

    def test_single_leaf2(self):
        leaf = TMTree("leaf", [], 50)
        leaf.update_rectangles((0,0,10,20))
        self.assertEqual(leaf.get_tree_at_position((0,5)), leaf, "There is only one leaf in the displayed tree stasitied the condition thus you must return the leaf")

    def test_left_corner_no_expanded(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 50)
        root = TMTree("root", [leaf, leaf2], 0)
        root.update_rectangles((0,0,10,20))
        act = root.get_tree_at_position((0,0))
        self.assertEqual(act, leaf)

    def test_left_corner_expanded(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 50)
        root = TMTree("root", [leaf, leaf2], 0)
        root.update_rectangles((0,0,10,20))
        set_expanded(root)
        act = root.get_tree_at_position((0,0))
        self.assertEqual(act, leaf, "The leaf is the only qualified leaf in the DISPLAYED Tree"+ " YOUR RESULT IS " + act._name)

    def test_vertical_bottom(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 50)
        root = TMTree("root", [leaf, leaf2], 0)
        root.update_rectangles((0, 0, 10, 20))
        set_expanded(root)
        act = root.get_tree_at_position((10, 20))
        self.assertEqual(act, leaf2,
                         "The leaf2 is the only qualified leaf in the DISPLAYED Tree"+ " YOUR RESULT IS " + act._name)

    def test_vertical_intersection(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 50)
        root = TMTree("root", [leaf, leaf2], 0)
        root.update_rectangles((0, 0, 10, 20))
        set_expanded(root)
        act = (root.get_tree_at_position((5, 10)))
        self.assertEqual(act, leaf,
                         "The leaf is the only qualified leaf in the DISPLAYED Tree"+ " YOUR RESULT IS " + act._name)

    def test_horizontal_intersection(self):
        leaf = TMTree("leaf", [], 10)
        leaf2 = TMTree("leaf2", [], 50)
        root = TMTree("root", [leaf, leaf2], 0)
        root.update_rectangles((0, 0, 20, 10))
        set_expanded(root)
        act = root.get_tree_at_position((3, 10))
        self.assertEqual(act, leaf,
                         "The leaf is the only qualified leaf in the DISPLAYED Tree"+ " YOUR RESULT IS " + act._name)

    def test_two_leaf_left(self):
        leaf = TMTree("leaf", [], 10)
        leaf2 = TMTree("leaf2", [], 50)
        root = TMTree("root", [leaf, leaf2], 0)
        root.update_rectangles((0, 0, 20, 10))
        set_expanded(root)
        act = root.get_tree_at_position((3, 10))
        self.assertEqual(act, leaf,
                         "The leaf is the only qualified leaf in the DISPLAYED Tree" + " YOUR RESULT IS " + act._name)

    def test_two_rectangle_left(self):
        leaf = TMTree("leaf", [], 10)
        leaf2 = TMTree("leaf2", [], 40)
        leaf3 = TMTree("leaf3", [], 50)
        folderA = TMTree("folderA", [leaf, leaf2], 0)
        root = TMTree("root", [folderA, leaf3], 0)
        root.update_rectangles((0, 0, 20, 10))
        root._expanded = True
        exp = leaf2
        act = root.get_tree_at_position((3, 10))
        self.assertEqual(act, exp)

    def test_three_rectangle_horizontal(self):
        leaf = TMTree("leaf", [], 10)
        leaf2 = TMTree("leaf2", [], 40)
        leaf3 = TMTree("leaf3", [], 50)
        folderA = TMTree("folderA", [leaf, leaf2], 0)
        root = TMTree("root", [folderA, leaf3], 0)
        root.update_rectangles((0, 0, 20, 10))
        root._expanded = True
        folderA._expanded = True
        exp = leaf2
        act = root.get_tree_at_position((3, 10))
        self.assertEqual(act, exp,
                         "The leaf2 is the only qualified leaf in the DISPLAYED Tree YOUR RESULT IS " + act._name)

    def test_three_rectangle_intersection(self):
        leaf = TMTree("leaf", [], 10)
        leaf2 = TMTree("leaf2", [], 40)
        leaf3 = TMTree("leaf3", [], 50)
        folderA = TMTree("folderA", [leaf, leaf2], 0)
        root = TMTree("root", [folderA, leaf3], 0)
        root.update_rectangles((0, 0, 20, 10))
        root._expanded = True
        folderA._expanded = True
        exp = leaf
        act = root.get_tree_at_position((5, 2))
        self.assertEqual(act, exp,
                         "The leaf is the only qualified leaf in the DISPLAYED Tree YOUR RESULT IS " + act._name)

    def test_three_rectangle_intersection_2(self):
        leaf = TMTree("leaf", [], 10)
        leaf2 = TMTree("leaf2", [], 40)
        leaf3 = TMTree("leaf3", [], 50)
        folderA = TMTree("folderA", [leaf, leaf2], 0)
        root = TMTree("root", [folderA, leaf3], 0)
        root.update_rectangles((0, 0, 20, 10))
        root._expanded = True
        folderA._expanded = True
        exp = leaf
        act = root.get_tree_at_position((10, 2))
        self.assertEqual(act, exp,
                         "The leaf is the only qualified leaf in the DISPLAYED Tree YOUR RESULT IS " + act._name)

    def test_three_rectangle_intersection_3(self):
        leaf = TMTree("leaf", [], 10)
        leaf2 = TMTree("leaf2", [], 40)
        leaf3 = TMTree("leaf3", [], 50)
        folderA = TMTree("folderA", [leaf, leaf2], 0)
        root = TMTree("root", [leaf3, folderA], 0)
        root.update_rectangles((0, 0, 10, 18))
        root._expanded = True
        folderA._expanded = True
        exp = leaf3
        act = root.get_tree_at_position((9, 2))
        self.assertEqual(act, exp,
                         "The leaf3 is the only qualified leaf in the DISPLAYED Tree YOUR RESULT IS " + act._name)

    def test_three_rectangle_intersection_4(self):
        leaf = TMTree("leaf", [], 10)
        leaf2 = TMTree("leaf2", [], 40)
        leaf3 = TMTree("leaf3", [], 50)
        folderA = TMTree("folderA", [leaf, leaf2], 0)
        root = TMTree("root", [leaf3, folderA], 0)
        root.update_rectangles((0, 0, 20, 10))
        root._expanded = True
        folderA._expanded = True
        exp = leaf
        act = root.get_tree_at_position((11, 2))
        self.assertEqual(act, exp,
                         "The leaf is the only qualified leaf in the DISPLAYED Tree YOUR RESULT IS " + act._name)



    def test_four_square_intersection(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 50)
        leaf3 = TMTree("leaf3", [], 50)
        leaf4 = TMTree("leaf4", [], 50)
        internal1 = TMTree("internal1", [leaf, leaf2], 0)
        internal2 = TMTree("internal2", [leaf3, leaf4], 0)
        root = TMTree("root", [internal1, internal2], 0)
        rect = (0, 0, 100, 100)
        set_expanded(root)
        root.update_rectangles(rect)
        exp = leaf
        act = root.get_tree_at_position((10, 2))
        self.assertEqual(act, exp,
                         "The leaf is the only qualified leaf in the DISPLAYED Tree YOUR RESULT IS " + act._name)


class a2_test_change_size(unittest.TestCase):
    def test_up(self):
        leaf = TMTree("leaf", [], 50)
        leaf.update_rectangles((0, 0, 100, 100))
        leaf.change_size(0.1)
        exp = 55
        act = leaf.data_size
        self.assertEqual(act, exp,
                         "Expected " + str(exp) + " Your result is " + str(act))

    def test_up2(self):
        leaf = TMTree("leaf", [], 50)
        leaf.update_rectangles((0, 0, 100, 100))
        leaf.change_size(0.99)
        exp = 100
        act = leaf.data_size
        self.assertEqual(act, exp,
                         "Expected " + str(exp) + " Your result is " + str(act))

    def test_down(self):
        leaf = TMTree("leaf", [], 50)
        leaf.update_rectangles((0, 0, 100, 100))
        leaf.change_size(-0.1)
        exp = 45
        act = leaf.data_size
        self.assertEqual(act, exp,
                         "Expected " + str(exp) + " Your result is " + str(act))

    def test_down2(self):
        leaf = TMTree("leaf", [], 50)
        leaf.update_rectangles((0, 0, 100, 100))
        leaf.change_size(-0.99)
        exp = 1
        act = leaf.data_size
        self.assertEqual(act, exp,
                         "Expected " + str(exp) + " Your result is " + str(act))

    def test_change_folder(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 60)
        root = TMTree("root", [leaf, leaf2], 0)
        root.update_rectangles((0, 0, 100, 100))
        root.change_size(0.01)
        self.assertEqual(root.data_size, 112)

    def test_change_folder2(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 60)
        root = TMTree("root", [leaf, leaf2], 0)
        root.update_rectangles((0, 0, 100, 100))
        leaf.change_size(0.1)
        exp = 55
        act = leaf.data_size
        self.assertEqual(act, 55,
                         "Expected " + str(exp) + " Your result is " + str(act))
        self.assertEqual(root.data_size, 115,
                         "When you change the size of a leaf you should also update its parent")

    def test_change_folder3(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 60)
        root = TMTree("root", [leaf, leaf2], 0)
        root.update_rectangles((0, 0, 100, 100))
        leaf.change_size(-0.1)
        exp = 45
        act = leaf.data_size
        self.assertEqual(act, exp,
                         "Expected " + str(exp) + " Your result is " + str(
                             act))
        self.assertEqual(root.data_size, 105,
                         "When you change the size of a leaf you should update its parent also")

    def test_change_folder4(self):
        leaf = TMTree("leaf", [], 50)
        leaf2 = TMTree("leaf2", [], 60)
        root = TMTree("root", [leaf, leaf2], 0)
        root.update_rectangles((0, 0, 100, 100))
        leaf.change_size(-0.1)
        exp = 45
        act = leaf.data_size
        self.assertEqual(act, exp,
                         "Expected " + str(exp) + " Your result is " + str(
                             act))
        self.assertEqual(root.data_size, 105,
                         "When you change the size of a leaf you should update its parent also")


class a2_test_move(unittest.TestCase):
    def test_leaf(self):
        leaf = TMTree("leaf", [], 50)
        dest = TMTree("leaf", [], 60)
        root = TMTree("root", [dest, leaf], 0)
        root.update_rectangles((0, 0, 100, 100))
        leaf.move(dest)
        self.assertListEqual(leaf._subtrees, [],
                             "You cannot move a leaf to a leaf")

    def test_leaf2(self):
        leaf = TMTree("leaf", [], 60)
        leaf2 = TMTree("leaf2", [], 60)
        dest = TMTree("dest", [leaf2], 0)
        root = TMTree("root", [dest, leaf], 0)
        root.update_rectangles((0, 0, 100, 100))
        leaf.move(dest)
        assert len(dest._subtrees) == 2
        self.assertEqual(dest._subtrees[-1], leaf,
                         "You should add leaf as the last element of dest's subtrees")
        self.assertEqual(leaf._parent_tree, dest,
                         "You should connect leaf to the proper parent tree after you move it")
        self.assertEqual(dest.data_size, 120,
                         "You should also update the data size of dest")

    # def test_move_to_folder(self):
    #     leaf = TMTree("leaf", [], 60)
    #     folderA = TMTree("folderA", [leaf], 0)
    #     leaf2 = TMTree("leaf2", [], 60)
    #     folderB = TMTree("folderB", [leaf2], 0)
    #     root = TMTree("root", [folderB], 0)
    #     root.update_rectangles((0, 0, 100, 100))
    #     folderA.move(folderB)
    #     self.assertEqual(folderA.data_size, 60, "Nothing should change")
    #     self.assertEqual(folderB.data_size, 120, "Nothing should change")
    #     self.assertEqual(len(folderA._subtrees), 1, "Nothing should change")
    #     self.assertEqual(len(folderB._subtrees), 2, "Nothing should change")

    def test_move_to_folder2(self):
        leaf = TMTree("leaf", [], 10)
        leaf2 = TMTree("leaf2", [], 20)
        leaf3 = TMTree("leaf3", [], 30)
        folderA = TMTree("folderA", [leaf, leaf2, leaf3], 0)
        leaf4 = TMTree("leaf3", [], 60)
        leaf5 = TMTree("leaf4", [], 60)
        folderB = TMTree("folderB", [leaf4, leaf5], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root.update_rectangles((0, 0, 100, 100))
        root._expanded = True
        folderA._expanded = True
        folderB._expanded = True
        leaf2.move(folderB)
        root.update_rectangles((0, 0, 100, 100))
        assert len(folderA._subtrees) == 2 and len(folderB._subtrees) == 3
        self.assertEqual(leaf2._parent_tree, folderB,
                         "You should move to the correct parent tree")
        self.assertEqual(folderA.data_size, 40,
                         "You should update folderA's datasize")
        self.assertEqual(folderB.data_size, 140,
                         "You should update folderB's datasize")
        self.assertEqual(folderA.rect, (0, 0, 100, 22),
                         "You should update the rect of folderA")
        self.assertEqual(folderB.rect, (0, 22, 100, 78),
                         "You should update the rect of folderB")

    def test_move_to_folder3(self):
        leaf = TMTree("leaf", [], 60)
        folderA = TMTree("folderA", [leaf], 0)
        leaf2 = TMTree("leaf2", [], 60)
        folderB = TMTree("folderB", [leaf2], 0)
        root = TMTree("root", [folderA, folderB], 0)
        folderA._expanded = True
        folderB._expanded = True
        root._expanded = True
        root.update_rectangles((0, 0, 100, 100))
        leaf.move(folderB)
        root.update_rectangles((0, 0, 100, 100))

        assert len(folderB._subtrees) == 2
        self.assertEqual(folderB._subtrees[-1], leaf,
                         "You should add leaf as the last element of folderB")
        self.assertEqual(leaf._parent_tree, folderB,
                         "You should point to the correct parent")
        self.assertEqual(folderB.data_size, 120,
                         "You should update the data size of folderB")
        self.assertEqual(folderA.data_size, 0,
                         "You should update the data size of folderA")
        self.assertEqual(root.data_size, 120,
                         "The root size remain same here since you did make so many change")
        self.assertEqual(folderA.rect, (0, 0, 100, 0),
                         "You should also update the rectangle of folderA")
        self.assertEqual(folderB.rect, (0, 0, 100, 100),
                         "You should also update the rectangle of folderB")


class a2_task5_set_expanded(unittest.TestCase):
    def test_leaf(self):
        leaf = TMTree("leaf", [], 50)
        leaf.update_rectangles((0,0,100,100))
        leaf.expand()
        self.assertCountEqual([rect[0] for rect in leaf.get_rectangles()], [(0,0,100,100)])
        self.assertEqual(leaf._expanded, False, "You cannot expanded a leaf(A single File)")

    def test_single_folder(self):
        leaf = TMTree("leaf", [], 50)
        folder = TMTree("folder", [leaf], 50)
        folder.expand()
        self.assertEqual(folder._expanded, True,
                         "You can only expanded a folder")

    def test_multiple_folder(self):
        leaf = TMTree("leaf", [], 40)
        folderA = TMTree("folderA", [leaf], 0)
        leaf2 = TMTree("leaf2", [], 40)
        folderB = TMTree("folderB", [leaf2], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root.update_rectangles((0,0,100,100))
        root.expand()
        folderA.expand()
        self.assertCountEqual([rect[0]for rect in root.get_rectangles()], [(0,0,100,50), (0,50,100,50)])
        self.assertCountEqual([rect[0]for rect in folderA.get_rectangles()], [(0,0,100,50)])
        self.assertEqual(folderA._expanded, True, "You should change the expanded of folderA")
        self.assertEqual(root._expanded, True, "You should also change the parent of folderA to be True")
        self.assertEqual(folderB._expanded, True, "You should also change the sibling of folderA")

    def test_multiple_folder2(self):
        leaf = TMTree("leaf", [], 40)
        leaf3 = TMTree("leaf3", [], 20)
        folderC = TMTree("folderC", [leaf, leaf3], 0)
        folderA = TMTree("folderA", [folderC], 0)
        leaf2 = TMTree("leaf2", [], 40)
        folderB = TMTree("folderB", [leaf2], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root.update_rectangles((0,0,100,100))
        root.expand()
        folderA.expand()
        folderC.expand()
        self.assertCountEqual([rect[0] for rect in root.get_rectangles()], [(0,0,66,60), (66,0,34,60), (0,60,100,40)])
        self.assertCountEqual([rect[0] for rect in folderA.get_rectangles()], [(0,0,66,60), (66,0,34,60)])
        self.assertCountEqual([rect[0] for rect in folderC.get_rectangles()], [(0,0,66,60), (66,0,34,60)])
        self.assertEqual(folderC._expanded, True, "You should change the expaned of folderC")
        self.assertEqual(folderB._expanded, True,
                         "You should also change the sibiling of folderA")

    def test_multiple_folder3(self):
        leaf = TMTree("leaf", [], 40)
        folderC = TMTree("folderC", [leaf], 0)
        folderA = TMTree("folderA", [folderC], 0)
        leaf2 = TMTree("leaf2", [], 40)
        folderB = TMTree("folderB", [leaf2], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root._expanded = True
        root.update_rectangles((0,0,100,100))
        root.expand()
        folderB.expand()
        root.get_rectangles()
        self.assertCountEqual([rect[0] for rect in root.get_rectangles()], [(0,0,100,50),(0,50,100,50)])
        self.assertCountEqual([rect[0] for rect in folderB.get_rectangles()], [(0,50,100,50)])
        self.assertEqual(folderB._expanded, True, "You should change the expanded of folderB")
        self.assertEqual(leaf2._expanded, False, "You should not modifided the child of folderB")
        self.assertEqual(folderA._expanded, True,
                         "You should also change the sibiling of folderB")
        self.assertEqual(root._expanded, True,
                         "You should also change the parent of folderB to be True")
        self.assertEqual(folderC._expanded, True,
                         "You should also change the expanded of fodlerC")

    def test_multiple_folder4(self):
        leaf = TMTree("leaf", [], 40)
        leaf3 = TMTree("leaf3", [], 40)
        folderC = TMTree("folderC", [leaf, leaf3], 0)
        folderA = TMTree("folderA", [folderC], 0)
        leaf2 = TMTree("leaf2", [], 40)
        folderB = TMTree("folderB", [leaf2], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root.update_rectangles((0,0,120,100))
        root.expand()
        act = [rect[0] for rect in root.get_rectangles()]
        self.assertCountEqual(act,[(0, 0, 80, 50), (0, 50, 80, 50), (80, 0, 40, 100)])

    def test_multiple_folder6(self):
        leaf = TMTree("leaf", [], 40)
        leaf3 = TMTree("leaf3", [], 20)
        folderC = TMTree("folderC", [leaf, leaf3], 0)
        folderA = TMTree("folderA", [folderC], 0)
        leaf2 = TMTree("leaf2", [], 40)
        folderB = TMTree("folderB", [leaf2], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root._expanded = True
        root.update_rectangles((0,0,100,100))
        root.expand()
        folderA.expand()
        self.assertCountEqual([rect[0] for rect in folderA.get_rectangles()], [(0, 0, 66, 60), (66, 0, 34, 60)])
        folderC.expand()
        self.assertCountEqual([rect[0] for rect in folderC.get_rectangles()], [(0,0,66,60),(66,0,34,60)])
        self.assertCountEqual([rect[0] for rect in root.get_rectangles()], [(0,0,66,60),(66,0,34,60), (0,60,100,40)])
        self.assertCountEqual([rect[0] for rect in folderA.get_rectangles()], [(0,0,66,60),(66,0,34,60)])
        self.assertEqual(folderC._expanded, True, "You should not change the expaned of folderC")
        self.assertEqual(folderA._expanded, True,
                         "You should change the expanded of folderC's parent")
        self.assertEqual(root._expanded, True,
                         "You should also change the parent of folderA to be True")
        self.assertEqual(folderB._expanded, True,
                         "You should also change the sibiling of folderA")


    def test_multiple_folder5(self):
        leaf = TMTree("leaf", [], 40)
        leaf3 = TMTree("leaf3", [], 20)
        folderC = TMTree("folderC", [leaf, leaf3], 0)
        folderA = TMTree("folderA", [folderC], 0)
        leaf2 = TMTree("leaf2", [], 40)
        folderB = TMTree("folderB", [leaf2], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root._expanded = True
        root.update_rectangles((0,0,100,100))
        root.expand()
        folderA.expand()
        act = [rect[0] for rect in root.get_rectangles()]
        self.assertCountEqual(act, [(0, 0, 66, 60), (66, 0, 34, 60), (0, 60, 100, 40)])
        self.assertEqual(folderC._expanded, True, "You should also change the expaned of folderC")
        self.assertEqual(all(set_collapse(folderC)), False, "You should not modify node under folderA")
        self.assertEqual(folderA._expanded, True,
                         "You should change the expanded of folderC's parent")
        self.assertEqual(root._expanded, True,
                         "You should also change the parent of folderA to be True")
        self.assertEqual(folderB._expanded, True,
                         "You should not change the sibiling of folderA")


class a2_task5_test_expand_all(unittest.TestCase):
    def test_single_folder(self):
        leaf = TMTree("leaf", [], 50)
        folder = TMTree("folder", [leaf], 50)
        folder.expand_all()
        act = all(set_expanded(folder))
        folder.update_rectangles((0,0,100,100))
        rec = [rect[0] for rect in folder.get_rectangles()]
        self.assertCountEqual(rec, [(0,0,100,100)])
        self.assertEqual(act, True,
                         "You should change every internal node under folder")

    def test_internal_node(self):
        leaf = TMTree("leaf", [], 40)
        folderA = TMTree("folderA", [leaf], 0)
        leaf2 = TMTree("leaf2", [], 40)
        folderB = TMTree("folderB", [leaf2], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root.update_rectangles((0,0,100,100))
        root._expanded = True
        root.expand()
        folderA.expand_all()
        temp = set_expanded(folderA)
        temp.pop(0)
        act = all(temp)
        rec = [rect[0] for rect in root.get_rectangles()]
        self.assertCountEqual([rect[0] for rect in folderA.get_rectangles()], [(0,0,100,50)])
        self.assertCountEqual(rec, [(0,0,100,50),(0,50,100,50)])
        self.assertEqual(act, True, "You should change every internal under folderA")
        self.assertEqual(root._expanded, True, "You should change root's expaned to be True")
        self.assertEqual(folderB._expanded, True, "You should modify folderB's expanded")

    def test_internal_node2(self):
        leaf = TMTree("leaf", [], 40)
        folderA = TMTree("folderA", [leaf], 0)
        leaf2 = TMTree("leaf2", [], 40)
        folderB = TMTree("folderB", [leaf2], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root._expanded = True
        root.update_rectangles((0,0,100,100))
        root.expand()
        folderB.expand_all()
        act = all(set_expanded(folderB))
        self.assertEqual(act, True,
                         "You should change the expanded of folderB")
        self.assertEqual(folderA._expanded, True,
                         "You should modify folderA")
        self.assertCountEqual([rect[0] for rect in folderB.get_rectangles()], [(0,50,100,50)])
        self.assertCountEqual([rect[0] for rect in root.get_rectangles()], [(0,0,100,50), (0,50,100,50)])

    def test_internal_node3(self):
        leaf = TMTree("leaf", [], 40)
        leaf2 = TMTree("leaf2", [], 40)
        folderC = TMTree("folderC", [leaf, leaf2], 0)
        folderA = TMTree("folderA", [folderC], 0)
        leaf3 = TMTree("leaf3", [], 40)
        leaf4 = TMTree("leaf4", [], 40)
        folderB = TMTree("folderB", [leaf3, leaf4], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root.update_rectangles((0,0,100,100))
        root.expand()
        folderA.expand_all()
        rec = [rect[0] for rect in root.get_rectangles()]
        self.assertCountEqual(rec, [(0, 0, 50, 50), (50, 0, 50, 50), (0, 50, 50, 50), (50, 50, 50, 50)])
        self.assertCountEqual([rect[0] for rect in folderA.get_rectangles()], [(0,0,50,50), (50,0,50,50)])
        self.assertEqual(folderC._expanded, True, "You should change the expaned of folderC")
        self.assertEqual(folderA._expanded, True,
                         "You should change the expanded of folderC's parent")
        self.assertEqual(root._expanded, True,
                         "You should also change the parent of folderA to be True")
        self.assertEqual(folderB._expanded, True,
                         "You should also change the sibiling of folderA")

    def test_internal_node4(self):
        leaf = TMTree("leaf", [], 40)
        folderC = TMTree("folderC", [leaf], 0)
        folderA = TMTree("folderA", [folderC], 0)
        leaf2 = TMTree("leaf2", [], 40)
        leaf3 = TMTree("leaf3", [], 20)
        folderB = TMTree("folderB", [leaf2, leaf3], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root.update_rectangles((0,0,100,100))
        root.expand()
        folderA.expand()
        folderC.expand_all()
        rec = [rect[0] for rect in root.get_rectangles()]
        self.assertCountEqual(rec, [(0, 0, 100, 40), (0, 40, 66, 60), (66, 40, 34, 60)])
        self.assertCountEqual([rect[0] for rect in folderA.get_rectangles()], [(0,0,100,40)])
        self.assertCountEqual([rect[0] for rect in folderC.get_rectangles()], [(0,0,100,40)])
        self.assertEqual(folderC._expanded, True, "You should change the expaned of folderC")
        self.assertEqual(folderA._expanded, True,
                         "You should change the expanded of folderC's parent")
        self.assertEqual(folderB._expanded, True,
                         "You should also change the sibiling of folderA")

    def test_root(self):
        leaf = TMTree("leaf", [], 40)
        leaf2 = TMTree("leaf2", [], 40)
        folderA = TMTree("folderA", [leaf, leaf2], 0)
        leaf3 = TMTree("leaf3", [], 40)
        leaf4 = TMTree("leaf4", [], 40)
        folderB = TMTree("folderB", [leaf3, leaf4], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root.update_rectangles((0,0,100,100))
        root.expand_all()
        act = all(set_expanded(root))
        rec = [rect[0] for rect in root.get_rectangles()]
        self.assertEqual(act, True, "You should change every internal node under root to be True")
        self.assertCountEqual(rec, [(0,0,50,50), (50,0,50,50), (0,50,50,50), (50,50,50,50)])
        self.assertCountEqual([rect[0] for rect in folderA.get_rectangles()], [(0,0,50,50), (50,0,50,50)])
        self.assertCountEqual([rect[0] for rect in folderB.get_rectangles()], [(0,50,50,50), (50,50,50,50)])


class a2_task5_test_collapseall(unittest.TestCase):
    def test_leaf(self):
        leaf = TMTree("leaf", [], 50)
        leaf.collapse_all()
        self.assertEqual(leaf._expanded, False, "You should not change the leaf")

    def test_single_folder(self):
        leaf = TMTree("leaf", [], 50)
        folderA = TMTree("folderA", [leaf], 50)
        root = TMTree("root", [folderA], 0)
        root.update_rectangles((0,0,100,100))
        root.expand()
        folderA.expand()
        leaf.collapse_all()
        self.assertEqual(folderA._expanded, False, "This should change the expanded of folderA to False")
        self.assertEqual(root._expanded, False, "This should change the root")
        self.assertCountEqual(root.get_rectangles()[0][0], (0,0,100,100))

    def test_single_folder2(self):
        leaf = TMTree("leaf", [], 50)
        folderA = TMTree("folderA", [leaf], 50)
        root = TMTree("root", [folderA], 0)
        root.update_rectangles((0,0,100,100))
        root.expand()
        folderA.collapse_all()
        self.assertEqual(root._expanded, False,
                         "This has not effect on the root")
        self.assertCountEqual(root.get_rectangles()[0][0], (0,0,100,100))

    def test_folder(self):
        leaf = TMTree("leaf", [], 40)
        folderA = TMTree("folderA", [leaf], 0)
        leaf2 = TMTree("leaf2", [], 40)
        folderB = TMTree("folderB", [leaf2], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root.update_rectangles((0,0,100,100))
        root.expand()
        folderB.expand()
        leaf2.collapse_all()
        self.assertEqual(root._expanded, False, "You should set _expanded of every thing under root to False")
        rec = [rect[0] for rect in root.get_rectangles()]
        self.assertCountEqual(rec, [(0,0,100,100)])

    def test_multiple_folder(self):
        leaf = TMTree("leaf", [], 40)
        leaf2 = TMTree("leaf2", [], 40)
        folderA = TMTree("folderA", [leaf, leaf2], 0)
        leaf3 = TMTree("leaf3", [], 40)
        leaf4 = TMTree("leaf4", [], 40)
        folderB = TMTree("folderB", [leaf3, leaf4], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root.update_rectangles((0, 0, 100, 100))
        root.expand()
        folderA.expand()
        folderB.expand()
        leaf2.collapse_all()
        rec = [rect[0] for rect in root.get_rectangles()]
        self.assertCountEqual(rec, [(0,0,100,100)])
        self.assertEqual(root._expanded, False, "You should not modified root")

class a2_test_task5_collapse(unittest.TestCase):
    def test_leaf(self):
        leaf = TMTree("leaf", [], 50)
        leaf.collapse()
        self.assertEqual(leaf._expanded, False, "You should not change the leaf")

    def test_single_folder(self):
        leaf = TMTree("leaf", [], 50)
        folderA = TMTree("folderA", [leaf], 50)
        root = TMTree("root", [folderA], 0)
        root.update_rectangles((0,0,100,100))
        root.expand()
        folderA.expand()
        leaf.collapse()
        self.assertEqual(folderA._expanded, False, "This should change the expanded of folderA to False")
        self.assertEqual(root._expanded, True, "This should change the root")
        self.assertCountEqual(folderA.get_rectangles()[0][0], (0,0,100,100))

    def test_single_folder2(self):
        leaf = TMTree("leaf", [], 50)
        folderA = TMTree("folderA", [leaf], 50)
        root = TMTree("root", [folderA], 0)
        root.update_rectangles((0,0,100,100))
        root.expand()
        folderA.collapse()
        self.assertEqual(folderA._expanded, False,
                         "This has not effect on the folderA")
        self.assertEqual(root._expanded, False,
                         "This has not effect on the root")
        self.assertCountEqual(root.get_rectangles()[0][0], (0,0,100,100))


    def test_folder(self):
        leaf = TMTree("leaf", [], 40)
        folderA = TMTree("folderA", [leaf], 0)
        leaf2 = TMTree("leaf2", [], 40)
        folderB = TMTree("folderB", [leaf2], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root.update_rectangles((0,0,100,100))
        root.expand()
        folderB.expand()
        leaf2.collapse()
        self.assertCountEqual([rect[0] for rect in root.get_rectangles()],[(0,0,100,50), (0,50,100,50)])
        self.assertEqual(root._expanded, True, "You should set _expanded of every thing under root to False")
        rec = [rect[0] for rect in folderB.get_rectangles()]
        self.assertCountEqual(rec, [(0,50,100,50)])


    def test_multiple_folder(self):
        leaf = TMTree("leaf", [], 40)
        leaf2 = TMTree("leaf2", [], 40)
        folderA = TMTree("folderA", [leaf, leaf2], 0)
        leaf3 = TMTree("leaf3", [], 40)
        leaf4 = TMTree("leaf4", [], 40)
        folderB = TMTree("folderB", [leaf3, leaf4], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root.update_rectangles((0, 0, 100, 100))
        root.expand()
        folderA.expand()
        folderB.expand()
        leaf.collapse()
        rec = [rect[0] for rect in root.get_rectangles()]
        act = all(set_collapse(folderA))
        self.assertCountEqual(rec, [(0,0,100,50), (0,50,50,50), (50,50,50,50)])
        self.assertEqual(root._expanded, True, "You should not modified root")
        self.assertEqual(act, True, "You should set expanded of every thing under folderA be False")

class a2_test_collapseall(unittest.TestCase):
    def test_leaf(self):
        leaf = TMTree("leaf", [], 50)
        leaf.collapse_all()
        self.assertEqual(leaf._expanded, False, "You should not change the leaf")

    def test_single_folder(self):
        leaf = TMTree("leaf", [], 50)
        folderA = TMTree("folderA", [leaf], 50)
        root = TMTree("root", [folderA], 0)
        root.update_rectangles((0,0,100,100))
        root.expand()
        folderA.expand()
        leaf.collapse_all()
        self.assertEqual(folderA._expanded, False, "This should change the expanded of folderA to False")
        self.assertEqual(root._expanded, False, "This should change the root")
        self.assertCountEqual(root.get_rectangles()[0][0], (0,0,100,100))

    def test_single_folder2(self):
        leaf = TMTree("leaf", [], 50)
        folderA = TMTree("folderA", [leaf], 50)
        root = TMTree("root", [folderA], 0)
        root.update_rectangles((0,0,100,100))
        root.expand()
        folderA.collapse_all()
        self.assertEqual(folderA._expanded, False,
                         "This has not effect on the folderA")
        self.assertEqual(root._expanded, False,
                         "This has not effect on the root")
        self.assertCountEqual(root.get_rectangles()[0][0], (0,0,100,100))


    def test_folder(self):
        leaf = TMTree("leaf", [], 40)
        folderA = TMTree("folderA", [leaf], 0)
        leaf2 = TMTree("leaf2", [], 40)
        folderB = TMTree("folderB", [leaf2], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root.update_rectangles((0,0,100,100))
        root.expand()
        folderB.expand()
        leaf2.collapse_all()
        self.assertCountEqual([rect[0] for rect in root.get_rectangles()],[(0,0,100,100)])
        self.assertEqual(root._expanded, False, "You should set _expanded of every thing under root to False")


    def test_multiple_folder(self):
        leaf = TMTree("leaf", [], 40)
        leaf2 = TMTree("leaf2", [], 40)
        folderA = TMTree("folderA", [leaf, leaf2], 0)
        leaf3 = TMTree("leaf3", [], 40)
        leaf4 = TMTree("leaf4", [], 40)
        folderB = TMTree("folderB", [leaf3, leaf4], 0)
        root = TMTree("root", [folderA, folderB], 0)
        root.update_rectangles((0, 0, 100, 100))
        root.expand()
        folderA.expand()
        folderB.expand()
        leaf.collapse_all()
        rec = [rect[0] for rect in root.get_rectangles()]
        act = all(set_collapse(folderA))
        self.assertCountEqual(rec, [(0,0,100,100)])
        self.assertEqual(root._expanded, False, "You should not modified root")


t1 = TMTree('T1', [], 1)
t2 = TMTree('T2', [t1], 2)
t3 = TMTree('T3', [], 3)
t4 = TMTree('T4', [t3, t2], 4)
t5 = TMTree('T5', [], 5)
t6 = TMTree('T6', [], 6)
t7 = TMTree('T7', [t5], 7)
root = TMTree('root', [t4, t6, t7], 1)
class test_is_displayed_tree_leaf(unittest.TestCase):

    def test_root(self):
        self.assertEqual(root.is_displayed_tree_leaf(), False)
        self.assertEqual(t2.is_displayed_tree_leaf(), False)
        self.assertEqual(t4.is_displayed_tree_leaf(), False)
        self.assertEqual(t7.is_displayed_tree_leaf(), False)

    def test_leaf(self):
        self.assertEqual(t1.is_displayed_tree_leaf(), True)
        self.assertEqual(t3.is_displayed_tree_leaf(), True)
        self.assertEqual(t5.is_displayed_tree_leaf(), True)
        self.assertEqual(t6.is_displayed_tree_leaf(), True)

class test_get_path_string(unittest.TestCase):
    def test_leaf_path1(self):
        exp = 'root | T4 | T2 | T1(1) None'
        act = t1.get_path_string()
        self.assertEqual(act, exp)

    def test_leaf_path2(self):
        exp = 'root | T4 | T3(3) None'
        act = t3.get_path_string()
        self.assertEqual(act, exp)

    def test_leaf_path3(self):
        exp = 'root | T7 | T5(5) None'
        act = t5.get_path_string()
        self.assertEqual(act, exp)

    def test_leaf_path4(self):
        exp = 'root | T6(6) None'
        act = t6.get_path_string()
        self.assertEqual(act, exp)

    def test_root_path(self):
        exp = 'root(29) None'
        act = root.get_path_string()
        self.assertEqual(act, exp)

    def test_inner_node_path1(self):
        exp = 'root | T4 | T2(3) None'
        act = t2.get_path_string()
        self.assertEqual(act, exp)

    def test_inner_node_path2(self):
        exp = 'root | T4(10) None'
        act = t4.get_path_string()
        self.assertEqual(act, exp)

    def test_inner_node_path3(self):
        exp = 'root | T7(12) None'
        act = t7.get_path_string()
        self.assertEqual(act, exp)


# class test_moves_to_nested_dict(unittest.TestCase):
#     def test_one_game_one_step(self):
#         game = [['a']]
#         act = moves_to_nested_dict(game)
#         exp = {('a', 1): {}}
#         self.assertEqual(act, exp)

#     def test_one_game_multi_step(self):
#         game = [['a', 'b', 'c']]
#         act = moves_to_nested_dict(game)
#         exp = {('a', 0): {('b', 0): {('c', 1): {}}}}
#         self.assertEqual(act, exp)

#     def test_multi_games_one_step(self):
#         game = [['a'], ['b'], ['c']]
#         act = moves_to_nested_dict(game)
#         exp = {('a', 1): {}, ('b', 1): {}, ('c', 1): {}}
#         self.assertEqual(act, exp)

#     def test_multi_games_multi_step(self):
#         game = [['a', 'b', 'd'], ['b', 'e'], ['c', 'f', 'e', 'b'], ['e', 'd'], ['f', 'a']]
#         act = moves_to_nested_dict(game)
#         exp = {('a', 0): {('b', 0): {('d', 1): {}}},
#                 ('b', 0): {('e', 1): {}},
#                 ('c', 0): {('f', 0): {('e', 0): {('b', 1): {}}}},
#                 ('e', 0): {('d', 1): {}},
#                 ('f', 0): {('a', 1): {}}}
#         self.assertEqual(act, exp)


# class test_chess_tree(unittest.TestCase):
#     def test_simp_game_default(self):
#         game = [['a']]
#         ct = ChessTree(moves_to_nested_dict(game))
#         self.assertEqual(ct.data_size, 1)
#         self.assertEqual(ct.rect, None)
#         exp_path = '- | a (end)'
#         self.assertEqual( ct.expand_all().get_path_string(), exp_path)
#         self.assertEqual(ct.get_path_string(), '- (white to play)')

#     def test_multiStep_game_dafault(self):
#         game = [['a', 'b', 'c']]
#         ct = ChessTree(moves_to_nested_dict(game))
#         self.assertEqual(ct.data_size, 1)
#         self.assertEqual(ct.rect, None)
#         exp_path = '- | a | b | c (end)'
#         self.assertEqual( ct.expand_all().get_path_string(), exp_path)
#         self.assertEqual(ct.get_path_string(), '- (white to play)')

#     def test_simp_game_black(self):
#         game = [['a']]
#         ct = ChessTree(moves_to_nested_dict(game), white_to_play=False)
#         exp_path = '- | a (end)'
#         self.assertEqual( ct.expand_all().get_path_string(), exp_path)
#         self.assertEqual(ct.get_path_string(), '- (black to play)')

#     def test_multiStep_game_black(self):
#         game = [['a', 'b', 'c']]
#         ct = ChessTree(moves_to_nested_dict(game), white_to_play=False)
#         exp_path = '- | a | b | c (end)'
#         self.assertEqual(ct.expand_all().get_path_string(), exp_path)
#         self.assertEqual(ct.get_path_string(), '- (black to play)')

#     def test_simp_games_default(self):
#         game = [['a'], ['b'], ['c']]
#         ct = ChessTree(moves_to_nested_dict(game))
#         self.assertEqual(ct.data_size, 3)
#         exp_path = '- | c (end)'
#         self.assertEqual(ct.expand_all().get_path_string(), exp_path)

#     def test_multi_games_default(self):
#         game = [['a', 'b'], ['b', 'd'], ['c', 'e'], ['d'], ['f', 'c']]
#         ct = ChessTree(moves_to_nested_dict(game))
#         self.assertEqual(ct.data_size, 5)
#         exp_path = '- | f | c (end)'
#         self.assertEqual(ct.expand_all().get_path_string(), exp_path)

#     def test_last_move(self):
#         game = [['a', 'b'], ['b', 'd'], ['c', 'e'], ['d'], ['f', 'c']]
#         ct = ChessTree(moves_to_nested_dict(game), last_move='here')
#         exp_path = 'here | f | c (end)'
#         self.assertEqual(ct.expand_all().get_path_string(), exp_path)
#         self.assertEqual(ct.get_path_string(), 'here (white to play)')

#     def test_num_game_1(self):
#         game = [['a', 'b'], ['b', 'd'], ['c', 'e'], ['d'], ['f', 'c']]
#         ct = ChessTree(moves_to_nested_dict(game), num_games_ended=1)
#         self.assertEqual(ct.data_size, 6)
#         exp_path = '- | f | c (end)'
#         self.assertEqual(ct.expand_all().get_path_string(), exp_path)

#     def test_num_game_more(self):
#         game = [['a', 'b'], ['b', 'd'], ['c', 'e'], ['d'], ['f', 'c']]
#         ct = ChessTree(moves_to_nested_dict(game), num_games_ended=4)
#         self.assertEqual(ct.data_size, 9)
#         exp_path = '- | f | c (end)'
#         self.assertEqual(ct.expand_all().get_path_string(), exp_path)


if __name__ == '__main__':
    unittest.main(exit=False)
