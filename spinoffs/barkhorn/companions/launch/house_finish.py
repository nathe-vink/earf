"""The Tropos fronts' finish on a house-ground frame (launch/house-ground.json's `finish`, through studio/engine/finish.py,
as the speaker lane's render.py applies it). Usage (the CAD venv: scipy): house_finish.py RAW.png OUT.png"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '..', 'studio', 'engine'))
import finish as Fn
fin = json.load(open(os.path.join(HERE, 'house-ground.json')))['finish']
print(Fn.post(sys.argv[1], sys.argv[2], fin)['finish'])
