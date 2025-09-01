<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Contracts\HttpClient\HttpClientInterface;

#[Route('/acteurs', name: 'acteurs_')]
class ActeurController extends AbstractController
{

    
    private string $api = 'http://127.0.0.1:8000';
    public function __construct(private HttpClientInterface $http) {}




    #[Route('', name: 'index', methods: ['GET'])]
    public function index(Request $request): Response
    {
        $q = trim((string)$request->query->get('q', ''));

        try {
            if ($q !== '') {
                // Buscar 1 por ID
                $one = $this->http->request('GET', "{$this->api}/acteur/{$q}");
                if ($one->getStatusCode() === 200) {
                    $acteurs = [ $one->toArray() ];
                } else {
                    $acteurs = [];
                }
            } else {
                // Listar todos
                $res = $this->http->request('GET', "{$this->api}/acteurs");
                $acteurs = $res->toArray();
            }
        } catch (\Throwable $e) {
            $acteurs = [];
            $this->addFlash('error', 'Erreur lors de la récupération des acteurs.');
        }

        return $this->render('acteurs/index.html.twig', [
            'titre'   => 'Acteurs — CRUD',
            'acteurs' => $acteurs,
            'q'       => $q,
        ]);
    }




    #[Route('/nouveau', name: 'ajouter', methods: ['GET','POST'])]
    public function ajouter(Request $request): Response
    {
        if ($request->isMethod('POST')) {
            $payload = [
                'id'      => (int)$request->request->get('id'),
                'name'    => trim((string)$request->request->get('name')),
                'bio'     => trim((string)$request->request->get('bio')),
                'picture' => trim((string)$request->request->get('picture')),
            ];
            try {
                $res = $this->http->request('POST', "{$this->api}/acteurs", [
                    'json' => $payload,
                    'timeout' => 5,
                ]);
                if ($res->getStatusCode() >= 200 && $res->getStatusCode() < 300) {
                    $this->addFlash('success', "Acteur #{$payload['id']} créé.");
                    return $this->redirectToRoute('acteurs_index');
                }
                $this->addFlash('error', 'Erreur lors de la création.');
            } catch (\Throwable $e) {
                $this->addFlash('error', 'Erreur lors de la création.');
            }
        }

        return $this->render('acteurs/form.html.twig', [
            'titre' => 'Ajouter un acteur',
            'mode'  => 'create',
            'a'     => ['id'=>'','name'=>'','bio'=>'','picture'=>''],
        ]);
    }



    #[Route('/{id}/modifier', name: 'modifier', methods: ['GET','POST'])]
    public function modifier(int $id, Request $request): Response
    {
        // cargar datos actuales
        try {
            $base = $this->http->request('GET', "{$this->api}/acteur/{$id}");
            if ($base->getStatusCode() !== 200) {
                $this->addFlash('warning', "Acteur {$id} introuvable.");
                return $this->redirectToRoute('acteurs_index');
            }
            $a = $base->toArray();
        } catch (\Throwable $e) {
            $this->addFlash('error', 'Erreur lors du chargement.');
            return $this->redirectToRoute('acteurs_index');
        }

        if ($request->isMethod('POST')) {
            $payload = [
                'name'    => trim((string)$request->request->get('name')),
                'bio'     => trim((string)$request->request->get('bio')),
                'picture' => trim((string)$request->request->get('picture')),
            ];
            try {
                $res = $this->http->request('PUT', "{$this->api}/acteur/{$id}", [
                    'json' => $payload,
                    'timeout' => 5,
                ]);
                if ($res->getStatusCode() >= 200 && $res->getStatusCode() < 300) {
                    $this->addFlash('success', "Acteur {$id} modifié.");
                    return $this->redirectToRoute('acteurs_detail', ['id'=>$id]);
                }
                $this->addFlash('error', 'Erreur lors de la mise à jour.');
            } catch (\Throwable $e) {
                $this->addFlash('error', 'Erreur lors de la mise à jour.');
            }
        }

        return $this->render('acteurs/form.html.twig', [
            'titre' => "Modifier l’acteur #{$id}",
            'mode'  => 'update',
            'a'     => $a,
        ]);
    }

    #[Route('/{id}', name: 'detail', methods: ['GET'])]



    public function detail(int $id): Response
    {
        try {
            $res = $this->http->request('GET', "{$this->api}/acteur/{$id}");
            if ($res->getStatusCode() !== 200) {
                $this->addFlash('warning', "Acteur {$id} introuvable.");
                return $this->redirectToRoute('acteurs_index');
            }
            $a = $res->toArray();
        } catch (\Throwable $e) {
            $this->addFlash('error', 'Erreur lors du chargement.');
            return $this->redirectToRoute('acteurs_index');
        }

        return $this->render('acteurs/show.html.twig', [
            'titre' => "Acteur #{$id}",
            'a'     => $a,
        ]);
    }


    #[Route('/{id}/supprimer', name: 'supprimer', methods: ['POST'])]
    public function supprimer(int $id): Response
    {
        try {
            $this->http->request('DELETE', "{$this->api}/acteur/{$id}", ['timeout'=>5]);
            $this->addFlash('success', "Acteur {$id} supprimé.");
        } catch (\Throwable $e) {
            $this->addFlash('error', 'Erreur lors de la suppression.');
        }
        return $this->redirectToRoute('acteurs_index');
    }
}
